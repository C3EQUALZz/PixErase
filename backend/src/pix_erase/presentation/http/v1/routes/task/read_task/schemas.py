from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["success", "failure", "started", "retrying", "processing"]
    description: Annotated[str, Field(min_length=1, description="Description of the task")]
