from typing import Literal, Annotated

from pydantic import BaseModel, Field


class TaskSchemaResponse(BaseModel):
    status: Literal["success", "failure", "started", "retrying", "processing"]
    description: Annotated[str, Field(min_length=1, description="Description of the task")]
