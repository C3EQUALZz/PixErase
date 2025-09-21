from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich

activate_user_router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)


@activate_user_router.patch(
    "/id/{user_id}/activate/",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def activate_user_by_id_handler():
    ...
