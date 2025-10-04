from inspect import getdoc
from typing import Final, cast

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Security
from starlette import status

from pix_erase.application.commands.user.create_user import CreateUserCommandHandler, CreateUserCommand
from pix_erase.application.common.views.user.create_user import CreateUserView
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.create.schemas import (
    CreateUserSchemaRequest,
    CreateUserSchemaResponse
)

create_user_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["User"],
)


@create_user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(cookie_scheme)],
    summary="Handler for creating user by admin",
    description=getdoc(CreateUserCommandHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_409_CONFLICT: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def create_user_handler(
        schemas: CreateUserSchemaRequest,
        interactor: FromDishka[CreateUserCommandHandler]
) -> CreateUserSchemaResponse:
    command: CreateUserCommand = CreateUserCommand(
        email=cast(str, schemas.email),
        name=schemas.name,
        password=schemas.password,
        role=schemas.role,
    )

    view: CreateUserView = await interactor(command)

    return CreateUserSchemaResponse(
        id=view.user_id
    )
