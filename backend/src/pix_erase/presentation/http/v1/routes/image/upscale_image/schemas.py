from typing import Literal, Annotated

from pydantic import BaseModel, Field


class UpscaleImageRequestSchema(BaseModel):
    algorithm: Literal["AI", "NearestNeighbour"]
    scale: Annotated[int, Field(ge=2, le=8)]
