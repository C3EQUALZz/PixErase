import os
from collections.abc import AsyncIterator, Generator

import pytest
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from taskiq import AsyncBroker, InMemoryBroker
from testcontainers.minio import MinioContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.redis import RedisContainer

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtAlgorithm, JwtSecret
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.timer_utc import AuthSessionRefreshThreshold, AuthSessionTtlMin
from pix_erase.infrastructure.persistence.models.base import mapper_registry
from pix_erase.setup.bootstrap import (
    setup_configs,
    setup_exc_handlers,
    setup_http_middlewares,
    setup_http_routes,
    setup_map_tables,
    setup_task_manager_middlewares,
    setup_task_manager_tasks,
)
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pix_erase.setup.config.http import HttpClientConfig
from pix_erase.setup.config.rabbit import RabbitConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.config.settings import AppConfig
from pix_erase.setup.ioc import setup_providers
from pix_erase.web import lifespan


@pytest.fixture(scope="session")
def minio_container() -> Generator[MinioContainer, None, None]:
    minio_config = S3Config(**os.environ)

    with MinioContainer(
        "quay.io/minio/minio:RELEASE.2025-03-12T18-04-18Z",
        access_key=minio_config.aws_access_key_id,
        secret_key=minio_config.aws_secret_access_key,
        port=minio_config.port,
    ) as minio:
        client = minio.get_client()
        client.make_bucket(minio_config.images_bucket_name)
        yield minio


@pytest.fixture(scope="session")
def redis_container() -> Generator[RedisContainer, None, None]:
    redis_config = RedisConfig(**os.environ)

    with RedisContainer("redis:8.0.2-alpine", port=redis_config.port, password=redis_config.password) as redis:
        yield redis


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    db_config = PostgresConfig(**os.environ)

    with PostgresContainer(
        image="postgres:16.10-alpine3.22",
        username=db_config.user,
        password=db_config.password,
        dbname=db_config.db_name,
        driver=db_config.driver,
        port=db_config.port,
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def rabbitmq_container() -> Generator[RabbitMqContainer, None, None]:
    rabbit_config = RabbitConfig(**os.environ)
    with RabbitMqContainer(
        image="rabbitmq:4.0",
        port=rabbit_config.port,
        username=rabbit_config.user,
        password=rabbit_config.password,
    ) as rabbit:
        yield rabbit


@pytest.fixture(scope="session")
def configs(
    postgres_container: PostgresContainer,
    redis_container: RedisContainer,
    minio_container: MinioContainer,
) -> AppConfig:
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(int(os.environ["POSTGRES_PORT"]))

    redis_host = redis_container.get_container_host_ip()
    redis_port = redis_container.get_exposed_port(int(os.environ["REDIS_PORT"]))

    minio_host = minio_container.get_container_host_ip()
    minio_port = minio_container.get_exposed_port(int(os.environ["MINIO_PORT"]))

    os.environ["REDIS_HOST"] = redis_host
    os.environ["REDIS_PORT"] = str(redis_port)

    os.environ["POSTGRES_HOST"] = host
    os.environ["POSTGRES_PORT"] = str(port)
    os.environ["MINIO_HOST"] = minio_host
    os.environ["MINIO_PORT"] = str(minio_port)

    return AppConfig()


@pytest.fixture(scope="session")
def broker(configs: AppConfig) -> AsyncBroker:
    task_manager: AsyncBroker = InMemoryBroker(await_inplace=True)

    task_manager_with_middlewares: AsyncBroker = setup_task_manager_middlewares(
        broker=task_manager,
        taskiq_config=configs.worker,
    )

    setup_task_manager_tasks(broker=task_manager_with_middlewares)

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

    setup_dishka_taskiq(container, broker=task_manager)

    return task_manager


@pytest.fixture(scope="session")
async def app(broker: AsyncBroker) -> AsyncIterator[FastAPI]:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        debug=True,
    )
    configs = setup_configs()
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
        AsyncBroker: broker,
        HttpClientConfig: configs.http,
    }
    container = make_async_container(*setup_providers(), context=context)
    setup_map_tables()
    setup_http_routes(app)
    setup_exc_handlers(app)
    setup_http_middlewares(app, api_config=configs.asgi)
    setup_dishka_fastapi(container, app)

    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield app

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    t = ASGITransport(app)
    async with AsyncClient(transport=t, base_url="http://test") as ac:
        yield ac
