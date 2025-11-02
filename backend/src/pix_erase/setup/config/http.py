from typing import Final

from pydantic import BaseModel, Field, field_validator

HTTP_TIMEOUT_MIN: Final[float] = 0.1
HTTP_CONNECTIONS_MIN: Final[int] = 1
HTTP_KEEPALIVE_EXPIRY_MIN: Final[float] = 0.1


class HttpClientConfig(BaseModel):
    default_timeout: float = Field(alias="DEFAULT_HTTP_TIMEOUT", default=30.0, validate_default=True)

    verify: bool | str = Field(alias="DEFAULT_HTTP_VERIFY", default=True, validate_default=True)
    follow_redirects: bool = Field(alias="DEFAULT_HTTP_FOLLOW_REDIRECTS", default=True, validate_default=True)
    http2: bool = Field(alias="DEFAULT_HTTP_HTTP2", default=False, validate_default=True)

    client_cert_path: str | None = Field(alias="DEFAULT_HTTP_CLIENT_CERT", default=None, validate_default=True)
    client_key_path: str | None = Field(alias="DEFAULT_HTTP_CLIENT_KEY", default=None, validate_default=True)
    proxy: str | None = Field(alias="DEFAULT_HTTP_PROXIES", default=None, validate_default=True)

    max_connections: int = Field(alias="DEFAULT_HTTP_MAX_CONNECTIONS", default=100, validate_default=True)
    max_keepalive_connections: int = Field(alias="DEFAULT_HTTP_MAX_KEEPALIVE", default=20, validate_default=True)
    keepalive_expiry: float = Field(alias="DEFAULT_HTTP_KEEPALIVE_EXPIRY", default=5.0, validate_default=True)

    @field_validator("default_timeout")
    @classmethod
    def validate_default_timeout(cls, v: float) -> float:
        if v < HTTP_TIMEOUT_MIN:
            raise ValueError(
                f"DEFAULT_HTTP_TIMEOUT must be at least {HTTP_TIMEOUT_MIN} seconds, got {v}."
            )
        return v

    @field_validator("max_connections", "max_keepalive_connections")
    @classmethod
    def validate_max_connections(cls, v: int) -> int:
        if v < HTTP_CONNECTIONS_MIN:
            raise ValueError(
                f"HTTP max connections must be at least {HTTP_CONNECTIONS_MIN}, got {v}."
            )
        return v

    @field_validator("keepalive_expiry")
    @classmethod
    def validate_keepalive_expiry(cls, v: float) -> float:
        if v < HTTP_KEEPALIVE_EXPIRY_MIN:
            raise ValueError(
                f"DEFAULT_HTTP_KEEPALIVE_EXPIRY must be at least {HTTP_KEEPALIVE_EXPIRY_MIN} seconds, got {v}."
            )
        return v
