from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class GrayScaleImageSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: Annotated[
        str,
        Field(
            title="Task ID",
            description="The unique task id that process request from user",
            examples=["grayscale_image:75079971-fb0e-4e04-bf07-ceb57faebe84"],
            min_length=1,
            pattern=r"^grayscale_image:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        )
    ]
