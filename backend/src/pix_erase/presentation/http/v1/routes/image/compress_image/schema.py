from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CompressImageRequestSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

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


class CompressImageResponseSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: Annotated[
        str,
        Field(
            title="Task ID",
            description="The unique task id that process request from user",
            examples=["compress_image:75079971-fb0e-4e04-bf07-ceb57faebe84"],
            min_length=1,
            pattern=r"^compress_image:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        )
    ]
