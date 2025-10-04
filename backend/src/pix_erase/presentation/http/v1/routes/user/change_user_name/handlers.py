from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path, Body, Security

from pix_erase.application.commands.user.change_user_name import (
    ChangeUserNameByIDCommandHandler,
    ChangeUserNameByIDCommand
)
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

change_user_name_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute
)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)

NameBodyParameter = Body(
    title="User name",
    description="The name of the user to get.",
    examples=["super-bagratus"],
    min_length=5,
)


@change_user_name_router.patch(
    "/id/{user_id}/name/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Changes user name",
    description=getdoc(ChangeUserNameByIDCommandHandler),
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def change_user_name_by_id_handler(
        user_id: Annotated[UUID, UserIDPathParameter],
        name: Annotated[str, NameBodyParameter],
        interactor: FromDishka[ChangeUserNameByIDCommandHandler]
) -> None:
    command: ChangeUserNameByIDCommand = ChangeUserNameByIDCommand(
        user_id=user_id,
        new_name=name
    )

    await interactor(command)
