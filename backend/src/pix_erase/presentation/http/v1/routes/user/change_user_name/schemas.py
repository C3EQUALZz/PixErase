from pydantic import BaseModel, Field, BeforeValidator, AfterValidator
from typing import Annotated


class ChangeUserNameRequestSchema(BaseModel):
    name: Annotated[
        str,
        BeforeValidator(lambda x: str.strip(str(x))),
        Field(
            title="User name",
            description="The name of the user to get.",
            examples=["super-bagratus"],
            min_length=5
        ),
        AfterValidator(lambda x: str.strip(str(x))),
    ]
