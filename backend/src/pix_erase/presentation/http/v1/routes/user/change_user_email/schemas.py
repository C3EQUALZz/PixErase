from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, BeforeValidator, AfterValidator


class ChangeUserEmailSchemaRequest(BaseModel):
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda x: str.strip(str(x))),
        Field(
            title="User email",
            description="The email of the user to get.",
            examples=["super-bagratus2013@gmail.com"]
        ),
        AfterValidator(lambda x: str.strip(str(x))),
    ]
