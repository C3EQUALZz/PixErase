from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class RotateImageSchemaRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    angle: Annotated[
        int,
        Field(
            title="Angle for rotating",
            description="The angle value for rotating image",
            examples=[0, 360, 120, 180, -120],
        )
    ]


class RotateImageSchemaResponse(BaseModel):
    task_id: Annotated[
        str,
        Field(
            title="Task ID",
            description="The unique task id that process request from user",
            examples=["rotate_image:75079971-fb0e-4e04-bf07-ceb57faebe84"],
            min_length=1,
            pattern=r"^rotate_image:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        )
    ]
