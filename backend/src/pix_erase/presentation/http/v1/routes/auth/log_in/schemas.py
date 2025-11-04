from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginSchemaRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr = Field(..., description="Email address for user login")
    password: str = Field(..., description="Password for user login")
