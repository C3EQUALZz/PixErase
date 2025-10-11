from typing import Literal

from pydantic import BaseModel

from pix_erase.domain.image.values.image_id import ImageID


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
    scale: int


class RemoveBackgroundImageSchemaRequestTask(BaseModel):
    image_id: ImageID
