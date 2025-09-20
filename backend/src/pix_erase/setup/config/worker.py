from pydantic import BaseModel, Field


class TaskIQWorkerConfig(BaseModel):
    default_retry_count: int = Field(default=5, description="Default retry count if task fails")
    default_delay: int = Field(default=10, description="Default delay for next try if task fails")
    use_jitter: bool = Field(default=True, description="Use jitter for task fails")
    use_delay_exponent: bool = Field(default=True, description="Use exponent for task fails")
    max_delay_component: int = Field(default=120, description="Max delay component for task fails")