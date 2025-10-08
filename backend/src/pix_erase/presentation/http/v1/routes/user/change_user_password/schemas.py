from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator, AfterValidator


class ChangeUserPasswordRequestSchema(BaseModel):
    password: Annotated[
        str,
        BeforeValidator(lambda x: str.strip(str(x))),
        Field(
            min_length=8,
            max_length=255,
            title="The password of the user to get",
            description="The password of the user to get.",
            examples=["super-bagratus"]
        ),
        AfterValidator(lambda x: str.strip(str(x))),
    ]
