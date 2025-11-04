from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateImageSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    image_id: Annotated[UUID, Field(description="ID for new image")]
