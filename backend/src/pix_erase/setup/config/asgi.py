from pydantic import BaseModel, Field


class ASGIConfig(BaseModel):
    """Configuration container for ASGI server settings.

    Attributes:
        host: Interface to bind the server to (e.g., '0.0.0.0' or 'localhost').
        port: TCP port to listen on.
    """

    host: str = Field(
        alias="UVICORN_HOST",
        default="0.0.0.0",
        description="Interface to bind the server to (e.g., '0.0.0.0' or 'localhost').",
        validate_default=True,
    )
    port: int = Field(
        alias="UVICORN_PORT",
        default=8080,
        description="TCP port to listen on.",
        validate_default=True,
    )
    fastapi_debug: bool = Field(
        alias="FASTAPI_DEBUG",
        default=True,
        description="Enable fastapi debug output.",
        validate_default=True,
    )
    allow_credentials: bool = Field(
        alias="FASTAPI_ALLOW_CREDENTIALS",
        default=False,
        description="Enable fastapi allow credentials.",
        validate_default=True,
    )
    allow_methods: list[str] = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
    allow_headers: list[str] = [
        "Authorization",
        "Content-Type",
        "Cache-Control",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ]