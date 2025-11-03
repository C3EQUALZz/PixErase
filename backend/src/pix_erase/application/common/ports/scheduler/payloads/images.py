from dataclasses import dataclass
from typing import Literal

from pix_erase.application.common.ports.scheduler.payloads.base import TaskPayload
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_scale import ImageScale


@dataclass(frozen=True)
class CompressImagePayload(TaskPayload):
    image_id: ImageID
    quality: int


@dataclass(frozen=True)
class GrayScaleImagePayload(TaskPayload):
    image_id: ImageID


@dataclass(frozen=True)
class RotateImagePayload(TaskPayload):
    image_id: ImageID
    angle: int


@dataclass(frozen=True)
class UpscaleImagePayload(TaskPayload):
    image_id: ImageID
    algorithm: Literal["AI", "NearestNeighbour"]
    scale: ImageScale


@dataclass(frozen=True)
class RemoveImageBackgroundPayload(TaskPayload):
    image_id: ImageID


@dataclass(frozen=True)
class CompareImagesPayload(TaskPayload):
    first_image_id: ImageID
    second_image_id: ImageID