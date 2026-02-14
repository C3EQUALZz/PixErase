import asyncio
import logging
import sys
from typing import TYPE_CHECKING, Final

import grpc.aio
from dishka import make_async_container
from dishka.integrations.grpcio import DishkaAioInterceptor
from sqlalchemy.orm import clear_mappers

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtAlgorithm, JwtSecret
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.timer_utc import AuthSessionRefreshThreshold, AuthSessionTtlMin
from pix_erase.setup.bootstrap import (
    setup_configs,
    setup_grpc_interceptors,
    setup_grpc_reflection,
    setup_grpc_servicers,
    setup_map_tables,
)
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pix_erase.setup.config.http import HttpClientConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.ioc import setup_grpc_providers

if TYPE_CHECKING:
    from pix_erase.setup.config.settings import AppConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def serve() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    configs: AppConfig = setup_configs()
    setup_map_tables()

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
        HttpClientConfig: configs.http,
    }

    container = make_async_container(*setup_grpc_providers(), context=context)

    interceptors = setup_grpc_interceptors()
    interceptors.append(DishkaAioInterceptor(container))

    server = grpc.aio.server(interceptors=interceptors)
    setup_grpc_servicers(server)
    setup_grpc_reflection(server)

    address = f"{configs.grpc.host}:{configs.grpc.port}"
    server.add_insecure_port(address)

    logger.info("Starting gRPC server on %s", address)
    await server.start()

    try:
        await server.wait_for_termination()
    finally:
        logger.info("Shutting down gRPC server")
        await server.stop(grace=5)
        clear_mappers()
        await container.close()


if __name__ == "__main__":
    asyncio.run(serve())
