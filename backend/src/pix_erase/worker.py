from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from sqlalchemy.orm import clear_mappers
from taskiq import AsyncBroker, TaskiqEvents, TaskiqState

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtSecret, JwtAlgorithm
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.timer_utc import AuthSessionRefreshThreshold, AuthSessionTtlMin
from pix_erase.setup.bootstrap import setup_map_tables, setup_task_manager
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.ioc import setup_providers


async def startup(state: TaskiqState) -> None:  # noqa: ARG001
    setup_map_tables()


async def shutdown(state: TaskiqState) -> None:  # noqa: ARG001
    clear_mappers()


def create_taskiq_app() -> AsyncBroker:
    config: AppConfig = AppConfig()
    task_manager: AsyncBroker = setup_task_manager(
        taskiq_config=config.worker, rabbitmq_config=config.rabbitmq, redis_config=config.redis
    )

    task_manager.on_event(TaskiqEvents.WORKER_STARTUP)(startup)
    task_manager.on_event(TaskiqEvents.CLIENT_SHUTDOWN)(shutdown)

    context = {
        ASGIConfig: config.asgi,
        RedisConfig: config.redis,
        SQLAlchemyConfig: config.alchemy,
        PostgresConfig: config.postgres,
        JwtSecret: config.security.auth.jwt_secret,
        PasswordPepper: config.security.password.pepper,
        JwtAlgorithm: config.security.auth.jwt_algorithm,
        AuthSessionTtlMin: config.security.auth.session_ttl_min,
        AuthSessionRefreshThreshold: config.security.auth.session_refresh_threshold,
        CookieParams: CookieParams(secure=config.security.cookies.secure),
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)

    setup_dishka(container, broker=task_manager)

    return task_manager