from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field


class ChangeUserNameRequestSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: Annotated[
        str,
        BeforeValidator(lambda x: str.strip(str(x))),
        Field(title="User name", description="The name of the user to get.", examples=["super-bagratus"], min_length=5),
        AfterValidator(lambda x: str.strip(str(x))),
    ]
