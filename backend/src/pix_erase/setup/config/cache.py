from typing import Final

from pydantic import BaseModel, Field, RedisDsn, field_validator

from pix_erase.setup.config.consts import PORT_MAX, PORT_MIN

REDIS_DB_MIN: Final[int] = 0
REDIS_DB_MAX: Final[int] = 15
REDIS_MAX_CONNECTIONS_MIN: Final[int] = 1


class RedisConfig(BaseModel):
    host: str = Field(
        alias="REDIS_HOST",
        description="Redis host",
    )
    port: int = Field(
        alias="REDIS_PORT",
        description="Redis port",
    )
    user: str = Field(
        alias="REDIS_USER",
        description="Redis user",
    )
    password: str = Field(
        alias="REDIS_USER_PASSWORD",
        description="Redis password",
    )
    cache_db: int = Field(
        alias="REDIS_CACHE_DB",
        description="Redis db for caching results",
    )
    worker_db: int = Field(
        alias="REDIS_WORKER_DB",
        description="Redis db for worker results",
    )
    schedule_source_db: int = Field(
        alias="REDIS_SCHEDULE_SOURCE_DB",
        description="Redis db for schedule results",
    )
    max_connections: int = Field(
        default=20,
        alias="REDIS_MAX_CONNECTIONS",
        description="Redis max connections",
        validate_default=True
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"REDIS_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v

    @field_validator("cache_db", "worker_db", "schedule_source_db")
    @classmethod
    def validate_redis_db(cls, v: int) -> int:
        if not REDIS_DB_MIN <= v <= REDIS_DB_MAX:
            raise ValueError(
                f"Redis DB index must be between {REDIS_DB_MIN} and {REDIS_DB_MAX}, got {v}."
            )
        return v

    @field_validator("max_connections")
    @classmethod
    def validate_max_connections(cls, v: int) -> int:
        if v < REDIS_MAX_CONNECTIONS_MIN:
            raise ValueError(
                f"REDIS_MAX_CONNECTIONS must be at least {REDIS_MAX_CONNECTIONS_MIN}, got {v}."
            )
        return v

    @property
    def cache_uri(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=f"/{self.cache_db}"
            )
        )

    @property
    def worker_uri(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=f"/{self.worker_db}"
            )
        )

    @property
    def schedule_source_uri(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=f"/{self.schedule_source_db}"
            )
        )
