from pydantic import BaseModel, Field, field_validator

from pix_erase.setup.config.consts import PORT_MAX, PORT_MIN


class GrpcConfig(BaseModel):
    host: str = Field(
        alias="GRPC_HOST",
        default="0.0.0.0",  # nosec B104  # noqa: S104
        description="Interface to bind the gRPC server to.",
        validate_default=True,
    )
    port: int = Field(
        alias="GRPC_PORT",
        default=50051,
        description="TCP port for gRPC server.",
        validate_default=True,
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            msg = f"GRPC_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            raise ValueError(msg)
        return v
