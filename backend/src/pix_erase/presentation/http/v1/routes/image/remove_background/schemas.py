from typing import Annotated

from pydantic import BaseModel, Field


class RemoveBackgroundSchemaResponse(BaseModel):
    task_id: Annotated[
        str,
        Field(
            title="Task ID",
            description="The unique task id that process request from user",
            examples=["remove_background:75079971-fb0e-4e04-bf07-ceb57faebe84"],
            min_length=1,
            pattern=r"^remove_background+:[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        )
    ]
