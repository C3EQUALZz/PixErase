from pydantic import BaseModel, Field
from typing import Annotated


class RotateImageSchemaRequest(BaseModel):
    angle: Annotated[
        int,
        Field(
            title="Angle for rotating",
            description="The angle value for rotating image",
            examples=[0, 360, 120, 180, -120],
        )
    ]
