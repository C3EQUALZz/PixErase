from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

read_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"],
)


@read_image_router.get(
    "/id/{image_id}/",
    status_code=status.HTTP_200_OK,
)
async def read_image_by_id_handler():
    ...
