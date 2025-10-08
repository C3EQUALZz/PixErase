from typing import Annotated

from pydantic import BaseModel, Field


class CompressImageRequestSchema(BaseModel):
    quality: Annotated[
        int,
        Field(
            title="Quality of image in percents",
            description="The quality of image in percents, value must be positive",
            examples=[0, 30, 60, 90],
            ge=0,
            le=100
        )
    ]
