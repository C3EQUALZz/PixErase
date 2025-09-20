import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskiq import AsyncBroker, TaskiqScheduler
from taskiq.middlewares import SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from pix_erase.infrastructure.persistence.models.auth_sessions import map_auth_sessions_table
from pix_erase.infrastructure.persistence.models.users import map_users_table
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionHandler
from pix_erase.presentation.http.v1.common.routes import healthcheck, index
from pix_erase.presentation.http.v1.middlewares.asgi_auth import ASGIAuthMiddleware
from pix_erase.presentation.http.v1.middlewares.client_cache import ClientCacheMiddleware
from pix_erase.presentation.http.v1.middlewares.logs import LoggingMiddleware
from pix_erase.presentation.http.v1.routes.auth import router as auth_router
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.logs import LoggingConfig, build_structlog_logger
from pix_erase.setup.config.rabbit import RabbitConfig
from pix_erase.setup.config.redis import RedisConfig
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.config.worker import TaskIQWorkerConfig


@lru_cache(maxsize=1)
def setup_configs() -> AppConfig:
    return AppConfig()


def setup_map_tables() -> None:
    """
    Ensures imperative SQLAlchemy mappings are initialized at application startup.

    ### Purpose:
    In Clean Architecture, domain entities remain agnostic of database
    mappings. To integrate with SQLAlchemy, mappings must be explicitly
    triggered to link ORM attributes to domain classes. Without this setup,
    attempts to interact with unmapped entities in database operations
    will lead to runtime errors.

    ### Solution:
    This function provides a single entry point to initialize the mapping
    of domain entities to database tables. By calling the `setup_map_tables` function,
    ORM attributes are linked to domain classes without altering domain code
    or introducing infrastructure concerns.

    ### Usage:
    Call the `setup_map_tables` function in the application factory to initialize
    mappings at startup. Additionally, it is necessary to call this function
    in `env.py` for Alembic migrations to ensure all models are available
    during database migrations.
    """
    map_users_table()
    map_auth_sessions_table()


def setup_http_middlewares(app: FastAPI, /, api_config: ASGIConfig) -> None:
    """
    Registers all middlewares for FastAPI application.

    Args:
        app: FastAPI application
        api_config: ASGIConfig
    Returns:
        None
    """
    app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type, unused-ignore]
        allow_origins=[
            f"http://localhost:{api_config.port}",
            f"https://{api_config.host}:{api_config.port}",
        ],
        allow_credentials=api_config.allow_credentials,
        allow_methods=api_config.allow_methods,
        allow_headers=api_config.allow_headers,
    )
    app.add_middleware(ASGIAuthMiddleware)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(ClientCacheMiddleware, max_age=60)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type, unused-ignore]


def setup_http_routes(app: FastAPI, /) -> None:
    """
    Registers all routers for FastAPI application

    Args:
        app: FastAPI application

    Returns:
        None
    """
    app.include_router(index.router)
    app.include_router(healthcheck.router)

    router_v1: APIRouter = APIRouter(prefix="/v1")
    router_v1.include_router(auth_router)

    app.include_router(router_v1)


def setup_worker_broker(
        rabbit_config: RabbitConfig, redis_config: RedisConfig, worker_config: TaskIQWorkerConfig
) -> AsyncBroker:
    broker: AioPikaBroker = (
        AioPikaBroker(
            url=rabbit_config.uri,
            declare_exchange=True,
            declare_queues_kwargs={"durable": True},
            declare_exchange_kwargs={"durable": True},
        )
        .with_result_backend(RedisAsyncResultBackend(redis_url=redis_config.worker_uri))
        .with_middlewares(
            SmartRetryMiddleware(
                default_retry_count=worker_config.default_retry_count,
                default_delay=worker_config.default_delay,
                use_jitter=worker_config.use_jitter,
                use_delay_exponent=worker_config.use_delay_exponent,
                max_delay_exponent=worker_config.max_delay_component,
            )
        )
    )
    return broker


def setup_worker_tasks(broker: AsyncBroker) -> None: ...


def setup_exc_handlers(app: FastAPI, /) -> None:
    """
    Registers exception handlers for the FastAPI application.

    Args:
        app: FastAPI application instance to configure
    """
    exception_handler: ExceptionHandler = ExceptionHandler(app)
    exception_handler.setup_handlers()


def setup_scheduler(broker: AsyncBroker) -> TaskiqScheduler:
    return TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(broker)],
    )


def setup_logging(logger_config: LoggingConfig) -> None:
    build_structlog_logger(cfg=logger_config)

    root_logger: logging.Logger = logging.getLogger()
    sys.excepthook = global_exception_handler_with_traceback
    root_logger.info("Logger configured")


def global_exception_handler_with_traceback(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.exception("Error", exc_info=(exc_type, value, traceback))