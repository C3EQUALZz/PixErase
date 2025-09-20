from inspect import getdoc
from typing import TYPE_CHECKING, Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Security, APIRouter
from starlette import status

from pix_erase.application.auth.read_current_user import ReadCurrentUserHandler
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.read_by_id.schemas import ReadUserByIDResponse

if TYPE_CHECKING:
    from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView

router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(cookie_scheme)],
    response_model=ReadUserByIDResponse,
    description=getdoc(ReadCurrentUserHandler),
    summary="Gets current user in system, user must be authenticated"
)
async def read_user_by_id_handler(
        interactor: FromDishka[ReadCurrentUserHandler]
) -> ReadUserByIDResponse:
    view: ReadUserByIDView = await interactor()

    return ReadUserByIDResponse(
        id=view.user_id,
        email=view.email,  # type: ignore[arg-type, unused-ignore]
        name=view.name,
        role=view.role,  # type: ignore[arg-type, unused-ignore]
    )