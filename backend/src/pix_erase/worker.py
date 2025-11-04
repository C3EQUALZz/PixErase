from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from sqlalchemy.orm import clear_mappers
from taskiq import AsyncBroker, TaskiqEvents, TaskiqState

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtAlgorithm, JwtSecret
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.timer_utc import AuthSessionRefreshThreshold, AuthSessionTtlMin
from pix_erase.setup.bootstrap import (
    setup_map_tables,
    setup_task_manager,
    setup_task_manager_middlewares,
    setup_task_manager_tasks,
)
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pix_erase.setup.config.http import HttpClientConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.ioc import setup_providers


async def startup(state: TaskiqState) -> None:  # noqa: ARG001
    setup_map_tables()


async def shutdown(state: TaskiqState) -> None:  # noqa: ARG001
    clear_mappers()


def create_worker_taskiq_app() -> AsyncBroker:
    configs: AppConfig = AppConfig()
    task_manager: AsyncBroker = setup_task_manager(
        taskiq_config=configs.worker, rabbitmq_config=configs.rabbitmq, redis_config=configs.redis
    )
    task_manager_with_middlewares: AsyncBroker = setup_task_manager_middlewares(
        broker=task_manager,
        taskiq_config=configs.worker,
    )
    setup_task_manager_tasks(broker=task_manager_with_middlewares)

    task_manager.on_event(TaskiqEvents.WORKER_STARTUP)(startup)
    task_manager.on_event(TaskiqEvents.CLIENT_SHUTDOWN)(shutdown)

    context = {
        ASGIConfig: configs.asgi,
        RedisConfig: configs.redis,
        SQLAlchemyConfig: configs.alchemy,
        PostgresConfig: configs.postgres,
        JwtSecret: configs.security.auth.jwt_secret,
        PasswordPepper: configs.security.password.pepper,
        JwtAlgorithm: configs.security.auth.jwt_algorithm,
        AuthSessionTtlMin: configs.security.auth.session_ttl_min,
        AuthSessionRefreshThreshold: configs.security.auth.session_refresh_threshold,
        CookieParams: CookieParams(secure=configs.security.cookies.secure),
        S3Config: configs.s3,
        AsyncBroker: task_manager,
        HttpClientConfig: configs.http,
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)

    setup_dishka(container, broker=task_manager)

    return task_manager
