from inspect import getdoc
from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from pix_erase.application.auth.log_in import LogInData, LogInHandler
from pix_erase.presentation.http.v1.routes.auth.log_in.schemas import LoginSchemaRequest

log_in_router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@log_in_router.post(
    path="/login/",
    status_code=status.HTTP_204_NO_CONTENT,
    description=getdoc(LogInHandler),
    summary="Logins user in system",
)
async def login_handler(request_schema: LoginSchemaRequest, interactor: FromDishka[LogInHandler]) -> None:
    """
    - Open to everyone.
    - Authenticates registered user,
    sets a JWT access token with a session ID in cookies,
    and creates a session.
    - A logged-in user cannot log in again
    until the session expires or is terminated.
    - Authentication renews automatically
    when accessing protected routes before expiration.
    - If the JWT is invalid, expired, or the session is terminated,
    the user loses authentication.

    Args:
        request_schema: log in creation data containing:
            - email: User's email address. Email must be unique in system. Pydantic makes validation for format.
            - password: User's password for registration (8 - 255 characters).
        interactor: Injected LogInCommandHandler instance
    """
    command: LogInData = LogInData(email=str(request_schema.email), password=request_schema.password)

    await interactor(command)
