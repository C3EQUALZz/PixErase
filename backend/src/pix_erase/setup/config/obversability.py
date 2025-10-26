from pydantic import BaseModel, Field


class ObservabilityConfig(BaseModel):
    app_name: str = "PixErase"

    tracing_grpc_host: str = Field(alias="TEMPO_HOST", description="Host for tempo")
    tracing_grpc_port: int = Field(alias="TEMPO_GRPC_PORT", description="Port to listen on.")

    @property
    def tracing_grpc_uri(self) -> str:
        return f"http://{self.tracing_grpc_host}:{self.tracing_grpc_port}"
