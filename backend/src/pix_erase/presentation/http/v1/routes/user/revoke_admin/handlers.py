from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Security
from starlette import status

from pix_erase.application.commands.user.revoke_admin_by_id import (
    RevokeAdminByIDCommandHandler,
    RevokeAdminByIDCommand
)
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

revoke_admin_router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@revoke_admin_router.patch(
    "/id/{id}/revoke-admin/",
    dependencies=[Security(cookie_scheme)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke Administrator access",
    description=getdoc(RevokeAdminByIDCommandHandler)
)
async def revoke_admin_by_id_handler(
        user_id: Annotated[UUID, UserIDPathParameter],
        interactor: FromDishka[RevokeAdminByIDCommandHandler]
) -> None:
    command: RevokeAdminByIDCommand = RevokeAdminByIDCommand(
        user_id=user_id,
    )

    await interactor(command)
