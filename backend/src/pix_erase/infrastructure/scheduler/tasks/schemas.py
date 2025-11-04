from typing import Literal

from pydantic import BaseModel

from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_scale import ImageScale


class GrayscaleImageSchemaRequestTask(BaseModel):
    image_id: ImageID


class RotateImageSchemaRequestTask(BaseModel):
    image_id: ImageID
    angle: int


class CompressImageSchemaRequestTask(BaseModel):
    image_id: ImageID
    quality: int


class UpscaleImageSchemaRequestTask(BaseModel):
    image_id: ImageID
    algorithm: Literal["AI", "NearestNeighbour"]
    scale: ImageScale


class RemoveBackgroundImageSchemaRequestTask(BaseModel):
    image_id: ImageID


class CompareImagesSchemaRequestTask(BaseModel):
    first_image_id: ImageID
    second_image_id: ImageID
