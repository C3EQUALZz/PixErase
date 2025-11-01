from pydantic import BaseModel, Field


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
