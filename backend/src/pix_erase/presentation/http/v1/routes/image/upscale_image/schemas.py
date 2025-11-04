from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class UpscaleImageRequestSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    algorithm: Literal["AI", "NearestNeighbour"]
    scale: Annotated[int, Field(ge=2, le=8)]


class UpscaleImageSchemeResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: Annotated[
        str,
        Field(
            title="Task ID",
            description="The unique task id that process request from user",
            examples=["upscale_image:75079971-fb0e-4e04-bf07-ceb57faebe84"],
            min_length=1,
            pattern=r"^upscale_image:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
        ),
    ]
