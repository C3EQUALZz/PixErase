import os

from pydantic import BaseModel, Field

from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.database import PostgresConfig, SQLAlchemyConfig
from pix_erase.setup.config.logs import LoggingConfig
from pix_erase.setup.config.rabbit import RabbitConfig
from pix_erase.setup.config.cache import RedisConfig
from pix_erase.setup.config.s3 import S3Config
from pix_erase.setup.config.security import SecurityConfig, AuthSettings, CookiesSettings, PasswordSettings
from pix_erase.setup.config.worker import TaskIQWorkerConfig
from dotenv import load_dotenv

class AppConfig(BaseModel):
    load_dotenv(r"D:\PycharmProjects\PixErase\backend\.env")

    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging config",
    )
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
        description="Postgres settings",
    )
    alchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
        description="SQLAlchemy settings",
    )
    security: SecurityConfig = Field(
        default_factory=lambda: SecurityConfig(
            auth=AuthSettings(**os.environ),
            cookies=CookiesSettings(**os.environ),
            password=PasswordSettings(**os.environ),
        ),
        description="Security config",
    )
    rabbitmq: RabbitConfig = Field(
        default_factory=lambda: RabbitConfig(**os.environ),
        description="RabbitMQ settings",
    )
    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig(**os.environ),
        description="Redis settings",
    )
    worker: TaskIQWorkerConfig = Field(
        default_factory=lambda: TaskIQWorkerConfig(**os.environ),
        description="Worker settings",
    )
    asgi: ASGIConfig = Field(
        default_factory=lambda: ASGIConfig(**os.environ),
        description="ASGI settings",
    )
    s3: S3Config = Field(
        default_factory=lambda: S3Config(**os.environ),
        description="S3 settings",
    )