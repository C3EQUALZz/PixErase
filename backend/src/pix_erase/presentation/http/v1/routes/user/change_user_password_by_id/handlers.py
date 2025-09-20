from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Security, Path, Body
from starlette import status

from pix_erase.application.commands.user.change_user_password import (
    ChangeUserPasswordCommandHandler,
    ChangeUserPasswordCommand
)
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)

PasswordBodyParameter = Body(
    title="The password of the user to get",
    description="The password of the user to get.",
    examples=["super-bagratus"]
)


@router.patch(
    "/id/{user_id}/password",
    summary="Changes user password",
    description=getdoc(ChangeUserPasswordCommandHandler),
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(cookie_scheme)],
)
async def change_user_password_handler(
        user_id: Annotated[UUID, UserIDPathParameter],
        password: Annotated[str, PasswordBodyParameter],
        interactor: FromDishka[ChangeUserPasswordCommandHandler]
) -> None:
    command: ChangeUserPasswordCommand = ChangeUserPasswordCommand(
        user_id=user_id,
        password=password,
    )

    await interactor(command)
