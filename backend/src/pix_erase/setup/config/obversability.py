from pydantic import BaseModel, Field, field_validator

from pix_erase.setup.config.consts import PORT_MAX, PORT_MIN


class ObservabilityConfig(BaseModel):
    app_name: str = "PixErase"

    tracing_grpc_host: str = Field(alias="TEMPO_HOST", description="Host for tempo")
    tracing_grpc_port: int = Field(alias="TEMPO_GRPC_PORT", description="Port to listen on.")

    @field_validator("tracing_grpc_port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"TEMPO_GRPC_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v

    @property
    def tracing_grpc_uri(self) -> str:
        return f"http://{self.tracing_grpc_host}:{self.tracing_grpc_port}"
