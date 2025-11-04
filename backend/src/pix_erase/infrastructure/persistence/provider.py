import logging
from collections.abc import AsyncIterator
from typing import Final

from aioboto3 import Session
from aiobotocore.client import AioBaseClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from pix_erase.setup.config.database import (
    PostgresConfig,
    SQLAlchemyConfig,
)
from pix_erase.setup.config.s3 import S3Config

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def get_engine(
    postgres_config: PostgresConfig,
    alchemy_config: SQLAlchemyConfig,
) -> AsyncIterator[AsyncEngine]:
    """Creates and manages the lifecycle of an async SQLAlchemy engine.

    Args:
        postgres_config: PostgreSQL configuration
        alchemy_config: SQLAlchemy configuration

    Yields:
        AsyncEngine: Configured SQLAlchemy async engine instance

    Note:
        - Uses connection pooling
        - Sets 5-second connection timeout
        - Enables connection health checks (pool_pre_ping)
        - Automatically disposes the engine when done

    Example:
        async for engine in get_engine(config):
            # Use engine...
    """
    engine: AsyncEngine = create_async_engine(
        postgres_config.uri,
        echo=alchemy_config.echo,
        pool_size=alchemy_config.pool_size,
        max_overflow=alchemy_config.max_overflow,
        pool_pre_ping=alchemy_config.pool_pre_ping,
        pool_recycle=alchemy_config.pool_recycle,
        future=alchemy_config.future,
    )
    logger.debug("Async engine created with uri: %s", postgres_config.uri)
    yield engine
    logger.debug("Disposing async engine...")
    await engine.dispose()
    logger.debug("Engine is disposed.")


async def get_sessionmaker(
    engine: AsyncEngine,
    alchemy_config: SQLAlchemyConfig,
) -> async_sessionmaker[AsyncSession]:
    """Creates an async session factory bound to an engine.

    Args:
        engine: AsyncEngine instance to bind to the session factory
        alchemy_config: SQLAlchemy configuration

    Returns:
        async_sessionmaker: Configured session factory with:
            - autoflush disabled (default property)
            - expire_on_commit disabled (default property)

    Note:
        - The returned factory should be reused throughout the application
        - Disabling autoflush and expire_on_commit improves performance
        - Sessions should be short-lived (created per request)
    """
    async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=alchemy_config.auto_flush,
        expire_on_commit=alchemy_config.expire_on_commit,
    )
    logger.debug("Async session maker initialized.")
    return async_session_factory


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Provides an async database session context manager.

    Args:
        session_factory: Session factory to create new sessions from

    Yields:
        AsyncSession: A new async database session

    Note:
        - Automatically handles session cleanup
        - Sessions should be used within a single logical operation
        - Transactions should be explicitly committed or rolled back

    Example:
        async for session in get_session(session_factory):
            await session.execute(...)
    """
    logger.debug("Starting async session...")
    async with session_factory() as session:
        logger.debug("Async session started.")
        yield session
        logger.debug("Closing async session.")
    logger.debug("Async session closed.")


async def get_s3_session(s3_config: S3Config) -> AsyncIterator[Session]:
    yield Session(
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.region_name,
    )


async def get_s3_client(session: Session, s3_config: S3Config) -> AsyncIterator[AioBaseClient]:
    async with session.client("s3", endpoint_url=s3_config.uri, use_ssl=False) as s3:
        yield s3
