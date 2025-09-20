from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from starlette import status

from pix_erase.application.commands.user.grant_admin_by_id import (
    GrantAdminToUserByIDCommand,
    GrantAdminToUserByIDCommandHandler
)

router: Final[APIRouter] = APIRouter(
    tags=["User"],
    prefix="/user",
    route_class=DishkaRoute,
)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@router.patch(
    "/id/{id}/grant-admin",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Grant Administrator access",
    description=getdoc(GrantAdminToUserByIDCommandHandler)
)
async def grant_admin_to_user_by_id_handler(
        user_id: Annotated[UUID, UserIDPathParameter],
        interactor: FromDishka[GrantAdminToUserByIDCommandHandler],
) -> None:
    command: GrantAdminToUserByIDCommand = GrantAdminToUserByIDCommand(
        user_id=user_id,
    )

    await interactor(command)
