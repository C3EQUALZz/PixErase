from typing import Final, Iterable

from fastapi import APIRouter

from pix_erase.presentation.http.v1.routes.image.compress_image.handlers import compress_image_router
from pix_erase.presentation.http.v1.routes.image.create_image.handlers import create_image_router
from pix_erase.presentation.http.v1.routes.image.delete_image.handlers import delete_image_router
from pix_erase.presentation.http.v1.routes.image.grayscale_image.handlers import grayscale_image_router
from pix_erase.presentation.http.v1.routes.image.read_image.handlers import read_image_router
from pix_erase.presentation.http.v1.routes.image.rotate_image.handlers import rotate_image_router
from pix_erase.presentation.http.v1.routes.image.exif_image.handlers import exif_image_router

image_router: Final[APIRouter] = APIRouter(
    prefix="/image",
    tags=["Image"],
)

sub_routers: Final[Iterable[APIRouter]] = (
    rotate_image_router,
    compress_image_router,
    create_image_router,
    grayscale_image_router,
    delete_image_router,
    read_image_router,
    exif_image_router
)

for sub_router in sub_routers:
    image_router.include_router(sub_router)
