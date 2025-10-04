from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Mapping


@dataclass(eq=False)
class ImageInfo:
    width: int
    height: int
    is_animated: bool
    format: str | None = None
    camera_make: str | None = None
    camera_model: str | None = None
    exposure_time: str | None = None
    aperture: str | None = None
    focal_length: str | None = None
    iso: int | None = None
    created_date: datetime | None = None
    gps_info: Mapping[str, float] | None = None


class ImageInfoExtractor(Protocol):
    @abstractmethod
    async def extract(self, data: bytes) -> ImageInfo:
        ...
