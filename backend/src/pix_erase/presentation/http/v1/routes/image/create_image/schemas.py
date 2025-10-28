from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Annotated

class CreateImageSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    image_id: Annotated[UUID, Field(description="ID for new image")]
