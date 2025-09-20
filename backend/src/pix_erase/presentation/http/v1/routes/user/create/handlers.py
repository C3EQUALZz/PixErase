from inspect import getdoc
from typing import Final, cast

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Security
from starlette import status

from pix_erase.application.commands.user.create_user import CreateUserCommandHandler, CreateUserCommand
from pix_erase.application.common.views.user.create_user import CreateUserView
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.create.schemas import (
    CreateUserSchemaRequest,
    CreateUserSchemaResponse
)

router: Final[APIRouter] = APIRouter(
    prefix="/user",
    route_class=DishkaRoute,
    tags=["User"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(cookie_scheme)],
    summary="Handler for creating user by admin",
    description=getdoc(CreateUserCommandHandler)
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
