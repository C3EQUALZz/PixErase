import os
from typing import Final

from pydantic import BaseModel, Field, PostgresDsn, field_validator

PORT_MIN: Final[int] = 1
PORT_MAX: Final[int] = 65535


class PostgresConfig(BaseModel):
    """Configuration container for PostgreSQL database connection settings.

    Attributes:
        user: Database username.
        password: Database password.
        host: Database server hostname or IP address.
        port: Database server port.
        db_name: Name of the database to connect to.

    Properties:
        uri: Complete PostgreSQL connection URI in psycopg format.
    """

    user: str = Field(
        alias="POSTGRES_USER",
        description="Database username to connect",
    )
    password: str = Field(
        alias="POSTGRES_PASSWORD",
        description="Database password to connect",
    )
    host: str = Field(
        alias="POSTGRES_HOST",
        description="Database server hostname or IP address",
    )
    port: int = Field(
        alias="POSTGRES_PORT",
        description="Database server port",
    )
    db_name: str = Field(
        alias="POSTGRES_DB",
        description="Database name to connect",
    )
    driver: str = Field(
        alias="POSTGRES_DRIVER",
        description="Database driver",
    )

    @field_validator("host")
    @classmethod
    def override_host_from_env(cls, v: str) -> str:
        postgres_host_env = os.environ.get("POSTGRES_HOST")
        if postgres_host_env:
            return postgres_host_env
        return v

    @field_validator("port")
    @classmethod
    def validate_port_range(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(f"Port must be between {PORT_MIN} and {PORT_MAX}")
        return v


    @property
    def uri(self) -> str:
        """Generates a PostgreSQL connection URI.

        Returns:
            str: Connection string in format:
                postgresql+psycopg://user:password@host:port/db_name

        Note:
            - Uses psycopg driver for async operations
            - Includes all authentication credentials
            - Suitable for SQLAlchemy's create_async_engine
        """
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db_name,
            ),
        )


class SQLAlchemyConfig(BaseModel):
    """
    Configuration container for SQLAlchemy.
    """
    pool_pre_ping: bool = Field(
        alias="DB_POOL_PRE_PING",
        description="Enable database pool pre ping.",
    )
    pool_recycle: int = Field(
        alias="DB_POOL_RECYCLE",
        description="Time to live connection in minutes",
    )
    pool_size: int = Field(
        alias="DB_POOL_SIZE",
        description="Count of database connection pools",
    )
    max_overflow: int = Field(
        alias="DB_POOL_MAX_OVERFLOW",
        description="Count of database connection pools overflow",
    )
    echo: bool = Field(
        alias="DB_ECHO",
        description="Enable database echo mode for debugging.",
        validate_default=True,
    )
    auto_flush: bool = Field(
        alias="DB_AUTO_FLUSH",
        default=False,
        description="Enable database auto flush mode",
        validate_default=True,
    )
    expire_on_commit: bool = Field(
        alias="DB_EXPIRE_ON_COMMIT",
        default=False,
        description="Enable database expire on commit mode",
        validate_default=True,
    )
    future: bool = Field(
        alias="DB_FUTURE",
        default=True,
        description="Enable database future mode.",
        validate_default=True,
    )