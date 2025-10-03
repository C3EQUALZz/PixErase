from pydantic import BaseModel, Field
from uuid import UUID
from typing import Annotated

class CreateImageSchemaResponse(BaseModel):
    image_id: Annotated[UUID, Field(description="ID for new image")]
