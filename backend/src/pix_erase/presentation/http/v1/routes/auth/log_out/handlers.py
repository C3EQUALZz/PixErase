from inspect import getdoc
from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from pix_erase.application.auth.log_out import LogOutHandler

router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)


@router.delete(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    description=getdoc(LogOutHandler),
    summary="Log out user from system, removing data from cookie",
)
async def logout(interactor: FromDishka[LogOutHandler]) -> None:
    """
    - Open to authenticated users.
    - Logs the user out by deleting the JWT access token from cookies
    and removing the session from the database.

    Args:
        interactor: LogOutCommandHandler
    Returns:
        None
    """
    await interactor()