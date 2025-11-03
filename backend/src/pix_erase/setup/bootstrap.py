import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any, Final

from asgi_monitor.integrations.fastapi import TracingConfig, setup_tracing, MetricsConfig, setup_metrics
from asgi_monitor.logging import configure_logging
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from taskiq import AsyncBroker, TaskiqScheduler, async_shared_broker, ScheduleSource, PrometheusMiddleware
from taskiq.middlewares import SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend, ListRedisScheduleSource

from pix_erase.infrastructure.persistence.models.auth_sessions import map_auth_sessions_table
from pix_erase.infrastructure.persistence.models.image_comparisons import map_image_comparisons_table
from pix_erase.infrastructure.persistence.models.users import map_users_table
from pix_erase.infrastructure.scheduler.tasks.images_tasks import setup_images_task
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionHandler
from pix_erase.presentation.http.v1.common.routes import healthcheck, index
from pix_erase.presentation.http.v1.middlewares.asgi_auth import ASGIAuthMiddleware
from pix_erase.presentation.http.v1.middlewares.client_cache import ClientCacheMiddleware
from pix_erase.presentation.http.v1.middlewares.logs import LoggingMiddleware
from pix_erase.presentation.http.v1.routes.auth import auth_router
from pix_erase.presentation.http.v1.routes.image import image_router
from pix_erase.presentation.http.v1.routes.internet_protocol import ip_router
from pix_erase.presentation.http.v1.routes.task import task_router
from pix_erase.presentation.http.v1.routes.user import user_router
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig

from pix_erase.setup.config.obversability import ObservabilityConfig
from pix_erase.setup.config.rabbit import RabbitConfig
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.config.worker import TaskIQWorkerConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


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
    map_image_comparisons_table()


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
            f"http://127.0.0.1:{api_config.port}",
            f"http://127.0.0.1"
        ],
        allow_credentials=api_config.allow_credentials,
        allow_methods=api_config.allow_methods,
        allow_headers=api_config.allow_headers,
    )
    app.add_middleware(ASGIAuthMiddleware)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(ClientCacheMiddleware, max_age=60)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type, unused-ignore]


def setup_http_observability(
    app: FastAPI,
    /,
    observability_config: ObservabilityConfig,
) -> None:  # pragma: no cover
    configure_logging(
        level=logging.INFO,
        json_format=True,
        include_trace=True
    )
    sys.excepthook = global_exception_handler_with_traceback

    resource = Resource.create(
        attributes={
            "service.name": observability_config.app_name,
            "compose_service": observability_config.app_name,
        },
    )
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=observability_config.tracing_grpc_uri
            ),
        ),
    )
    trace_config = TracingConfig(tracer_provider=tracer_provider)
    setup_tracing(app=app, config=trace_config)

    metrics_config = MetricsConfig(
        app_name=observability_config.app_name,
        include_trace_exemplar=True,
    )
    setup_metrics(app=app, config=metrics_config)


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
    router_v1.include_router(user_router)
    router_v1.include_router(image_router)
    router_v1.include_router(task_router)
    router_v1.include_router(ip_router)

    app.include_router(router_v1)


def setup_task_manager(
        taskiq_config: TaskIQWorkerConfig, rabbitmq_config: RabbitConfig, redis_config: RedisConfig
) -> AsyncBroker:
    logger.debug("Creating taskiq broker for task management....")
    broker: AsyncBroker = (
        AioPikaBroker(
            url=rabbitmq_config.uri,
            declare_exchange=taskiq_config.declare_exchange,
            declare_queues_kwargs={"durable": taskiq_config.durable_queue},
            declare_exchange_kwargs={"durable": taskiq_config.durable_exchange},
        )
        .with_result_backend(RedisAsyncResultBackend(
            redis_url=redis_config.worker_uri,
            result_ex_time=1000,
        ))
    )
    logger.debug("Set async shared broker")
    async_shared_broker.default_broker(broker)

    logger.debug("Returning taskiq broker")
    return broker


def setup_task_manager_middlewares(
        broker: AsyncBroker, taskiq_config: TaskIQWorkerConfig
) -> AsyncBroker:
    logger.debug("Start setup broker middlewares")
    return broker.with_middlewares(
        SmartRetryMiddleware(
            default_retry_count=taskiq_config.default_retry_count,
            default_delay=taskiq_config.default_delay,
            use_jitter=taskiq_config.use_jitter,
            use_delay_exponent=taskiq_config.use_delay_exponent,
            max_delay_exponent=taskiq_config.max_delay_component,
        ),
        PrometheusMiddleware(
            server_addr=taskiq_config.prometheus_server_address,
            server_port=taskiq_config.prometheus_server_port
        )
    )


def setup_task_manager_tasks(broker: AsyncBroker) -> None:
    setup_images_task(broker=broker)


def setup_schedule_source(redis_config: RedisConfig) -> ScheduleSource:
    return ListRedisScheduleSource(url=redis_config.schedule_source_uri)


def setup_scheduler(broker: AsyncBroker, schedule_source: ScheduleSource) -> TaskiqScheduler:
    logger.debug("Creating taskiq scheduler for task management...")

    return TaskiqScheduler(
        broker=broker,
        sources=[
            LabelScheduleSource(broker),
            schedule_source,
        ],
    )


def setup_exc_handlers(app: FastAPI, /) -> None:
    """
    Registers exception handlers for the FastAPI application.

    Args:
        app: FastAPI application instance to configure
    """
    exception_handler: ExceptionHandler = ExceptionHandler(app)
    exception_handler.setup_handlers()


def global_exception_handler_with_traceback(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.exception("Error", exc_info=(exc_type, value, traceback))
