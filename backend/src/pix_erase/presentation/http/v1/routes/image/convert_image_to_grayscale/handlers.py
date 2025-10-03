from fastapi import APIRouter
from typing import Final

router: Final[APIRouter] = APIRouter()

@router.patch(
    "/id/{image_id}/grayscale/",
    s
)
async def convert_image_to_grayscale():
    ...
