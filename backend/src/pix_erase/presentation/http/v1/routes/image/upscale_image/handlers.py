from inspect import getdoc
from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from pix_erase.application.commands.image.upscale_image import UpscaleImageCommandHandler

upscale_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"]
)


@upscale_image_router.patch(
    "/id/{image_id}/upscale/ai/",
    status_code=status.HTTP_200_OK,
    summary="Upscale an image using ai at 2x times",
    description=getdoc(UpscaleImageCommandHandler),
    responses={}
)
async def upscale_image_handler(
        image_id: ...,
) -> None:
    ...
