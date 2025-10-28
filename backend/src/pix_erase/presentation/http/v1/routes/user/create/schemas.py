from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict
from uuid import UUID
from pix_erase.domain.user.values.user_role import UserRole


class CreateUserSchemaRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: Annotated[
        EmailStr,
        Field(
            description="User email address",
            examples=["ilovejava23@gmail.com"]
        )
    ]
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=5,
            max_length=255
        ),
        Field(
            description="User name",
            examples=["Egoryan Grishkov", "Bagrat Sarkisyan", "Denis Morozov"]
        )
    ]
    password: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=8,
            max_length=255
        ),
        Field(
            description="User password",
            examples=["SuperBobratus", "Denis Morozov"]
        )
    ]
    role: Annotated[
        UserRole,
        Field(
            description="User role",
            examples=["admin", "user"]
        )
    ]


class CreateUserSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        UUID,
        Field(
            description="User ID",
            examples=["08bde6f0-06c7-43f2-ab5d-d60ca062c5b5"]
        ),
    ]
