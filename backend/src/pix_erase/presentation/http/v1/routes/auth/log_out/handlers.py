from inspect import getdoc
from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Security

from pix_erase.application.auth.log_out import LogOutHandler
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

log_out_router: Final[APIRouter] = APIRouter(
    tags=["Auth"],
    route_class=DishkaRoute,
)


@log_out_router.delete(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    description=getdoc(LogOutHandler),
    summary="Log out user from system, removing data from cookie",
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
    }
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
