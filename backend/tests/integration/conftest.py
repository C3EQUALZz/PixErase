import os
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from taskiq import InMemoryBroker
from testcontainers.minio import MinioContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.redis import RedisContainer

from pix_erase.infrastructure.persistence.models.base import mapper_registry
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import PostgresConfig
from pix_erase.setup.config.rabbit import RabbitConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.config.settings import AppConfig


@pytest.fixture(scope="session")
def minio_container() -> Generator[MinioContainer, None, None]:
    minio_config = S3Config(**os.environ)

    with MinioContainer(
            "quay.io/minio/minio:RELEASE.2025-03-12T18-04-18Z",
            access_key=minio_config.aws_access_key_id,
            secret_key=minio_config.aws_secret_access_key,
            port=minio_config.port
    ) as minio:
        client = minio.get_client()
        client.make_bucket(minio_config.images_bucket_name)
        yield minio


@pytest.fixture(scope="session")
def redis_container() -> Generator[RedisContainer, None, None]:
    redis_config = RedisConfig(**os.environ)

    with RedisContainer(
            "redis:8.0.2-alpine",
            port=redis_config.port,
            password=redis_config.password
    ) as redis:
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
def config(
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


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_schema(container):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)


@pytest.fixture(scope="session")
def broker(config):
    broker = InMemoryBroker(await_inplace=True)
    # configure_broker(config=config, broker=broker)
    return broker
