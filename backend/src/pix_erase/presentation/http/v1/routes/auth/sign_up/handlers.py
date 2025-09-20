from inspect import getdoc
from typing import TYPE_CHECKING, Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from pix_erase.application.auth.sign_up import SignUpData, SignUpHandler
from pix_erase.presentation.http.v1.routes.auth.sign_up.schemas import (
    SignUpUserSchemaRequest,
    SignUpUserSchemaResponse,
)

if TYPE_CHECKING:
    from pix_erase.application.common.views.auth.sign_up import SignUpView

sign_up_router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@sign_up_router.post(
    path="/signup/",
    status_code=status.HTTP_201_CREATED,
    description=getdoc(SignUpHandler),
    summary="Sign up user in system",
    response_model=SignUpUserSchemaResponse
)
async def signup_handler(
    request_schema: SignUpUserSchemaRequest, interactor: FromDishka[SignUpHandler]
) -> SignUpUserSchemaResponse:
    """
    Create a new user record in the system. This handler works for all roles.

    Args:
        request_schema: New user creation data containing:
            - name: User's name (1-255 characters)
            - email: User's email address. Email must be unique in system. Pydantic makes validation for format.
            - password: User's password for registration (8 - 255 characters).
        interactor: Injected SignUpCommandHandler instance

    Returns:
        UUID: The unique id assigned to the new user

    Example:
        {
            "email": "manager@example.com",
            "name": "Manager",
            "password": "secure123",
            "role": "annotator"
        }
    """
    command: SignUpData = SignUpData(
        email=str(request_schema.email),
        name=request_schema.name,
        password=request_schema.password,
    )

    view: SignUpView = await interactor(data=command)

    return SignUpUserSchemaResponse(
        id=view.user_id,
    )