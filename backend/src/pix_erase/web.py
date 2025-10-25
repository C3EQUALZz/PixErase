import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final, cast

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import clear_mappers
from taskiq import AsyncBroker

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtSecret, JwtAlgorithm
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.timer_utc import AuthSessionTtlMin, AuthSessionRefreshThreshold
from pix_erase.setup.bootstrap import (
    setup_exc_handlers,
    setup_http_middlewares,
    setup_http_routes,
    setup_configs,
    setup_logging,
    setup_map_tables,
    setup_http_observability
)
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import SQLAlchemyConfig, PostgresConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.ioc import setup_providers
from pix_erase.worker import create_worker_taskiq_app

logger: Final[logging.Logger] = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Async context manager for FastAPI application lifecycle management.

    Handles the startup and shutdown events of the FastAPI application.
    Specifically ensures proper cleanup
        of Dishka container resources on shutdown.

    Args:
        app: FastAPI application instance. Positional-only parameter.

    Yields:
        None: Indicates successful entry into the context.

    Note:
        The actual resource cleanup (Dishka container closure)
            happens after yield, during the application shutdown phase.
    """
    setup_map_tables()
    task_manager: AsyncBroker = cast("AsyncBroker", app.state.task_manager)

    if not task_manager.is_worker_process:
        logger.info("Setting up taskiq")
        await task_manager.startup()

    yield

    if not task_manager.is_worker_process:
        logger.info("Shutting down taskiq")
        await task_manager.shutdown()

    clear_mappers()
    await cast("AsyncContainer", app.state.dishka_container).close()


def create_fastapi_app() -> FastAPI:  # pragma: no cover
    """Creates and configures a FastAPI application
        instance with all dependencies.

    Performs comprehensive application setup including:
    - Configuration initialization
    - Dependency injection container setup
    - Database mapping
    - Route registration
    - Exception handlers
    - Middleware stack
    - Dishka integration

    Returns:
        FastAPI: Fully configured application instance ready for use.

    Side Effects:
        - Configures global application state
        - Initializes database mappings
        - Sets up observability tools
        - Registers all route handlers
    """
    configs: AppConfig = setup_configs()

    setup_logging(logger_config=configs.logging)

    app: FastAPI = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        debug=configs.asgi.fastapi_debug,
        title=configs.asgi.app_name
    )

    task_manager: AsyncBroker = create_worker_taskiq_app()
    app.state.task_manager = task_manager

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
        AsyncBroker: task_manager
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)
    setup_http_routes(app)
    setup_exc_handlers(app)
    setup_http_middlewares(app, api_config=configs.asgi)
    setup_http_observability(app, config=configs.asgi)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app
