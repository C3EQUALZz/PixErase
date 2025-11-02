from typing import Final

from pydantic import BaseModel, Field, field_validator

from pix_erase.setup.config.consts import PORT_MAX, PORT_MIN

RETRY_COUNT_MIN: Final[int] = 0
DELAY_MIN: Final[int] = 0
MAX_DELAY_COMPONENT_MIN: Final[int] = 1


class TaskIQWorkerConfig(BaseModel):
    default_retry_count: int = Field(default=5, description="Default retry count if task fails")
    default_delay: int = Field(default=10, description="Default delay for next try if task fails")
    use_jitter: bool = Field(default=True, description="Use jitter for task fails")
    use_delay_exponent: bool = Field(default=True, description="Use exponent for task fails")
    max_delay_component: int = Field(default=120, description="Max delay component for task fails")
    durable_queue: bool = Field(default=True, description="Create durable queue for tasks or not")
    durable_exchange: bool = Field(default=True, description="Create exchange for tasks or not")
    declare_exchange: bool = Field(default=True, description="Declare exchange for tasks or not")

    prometheus_server_address: str = Field(
        alias="PROMETHEUS_WORKER_SERVER_HOST",
        description="Taskiq prometheus server address"
    )
    prometheus_server_port: int = Field(
        alias="PROMETHEUS_WORKER_SERVER_PORT",
        description="Taskiq prometheus server port"
    )

    @field_validator("default_retry_count")
    @classmethod
    def validate_default_retry_count(cls, v: int) -> int:
        if v < RETRY_COUNT_MIN:
            raise ValueError(
                f"default_retry_count must be at least {RETRY_COUNT_MIN}, got {v}."
            )
        return v

    @field_validator("default_delay")
    @classmethod
    def validate_default_delay(cls, v: int) -> int:
        if v < DELAY_MIN:
            raise ValueError(
                f"default_delay must be at least {DELAY_MIN} seconds, got {v}."
            )
        return v

    @field_validator("max_delay_component")
    @classmethod
    def validate_max_delay_component(cls, v: int) -> int:
        if v < MAX_DELAY_COMPONENT_MIN:
            raise ValueError(
                f"max_delay_component must be at least {MAX_DELAY_COMPONENT_MIN} seconds, got {v}."
            )
        return v

    @field_validator("prometheus_server_port")
    @classmethod
    def validate_prometheus_server_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"PROMETHEUS_WORKER_SERVER_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v
