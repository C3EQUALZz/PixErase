from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

activate_user_router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)


@activate_user_router.patch(
    "/id/{user_id}/activate/"
)
async def activate_user_by_id_handler():
    ...
