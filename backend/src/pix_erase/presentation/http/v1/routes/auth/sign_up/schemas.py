from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class SignUpUserSchemaRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr = Field(..., description="Email address of the user", examples=["john.smith@example.com"])
    name: str = Field(
        ...,
        description="Name of the user",
        min_length=1,
        max_length=255,
        examples=["john"],
    )
    password: str = Field(
        ..., description="Password for the user", min_length=8, max_length=255, examples=["super-puper-password-123"]
    )


class SignUpUserSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(..., description="UUID of the created user", examples=["0c8ba68a-299d-42d9-aca6-5b4056d3fd0f"])