from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol


class Orientation(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT = 4
    LEFT_TOP = 5
    RIGHT_TOP = 6
    RIGHT_BOTTOM = 7
    LEFT_BOTTOM = 8


class MeteringMode(Enum):
    UNKNOWN = 0
    AVERAGE = 1
    CENTER_WEIGHTED_AVERAGE = 2
    SPOT = 3
    MULTI_SPOT = 4
    PATTERN = 5
    PARTIAL = 6
    OTHER = 255


class WhiteBalance(Enum):
    AUTO = 0
    MANUAL = 1


class FlashMode(Enum):
    NO_FLASH = 0
    FIRED = 1
    FIRED_RETURN_NOT_DETECTED = 5
    FIRED_RETURN_DETECTED = 7
    AUTO_NO_FLASH = 8
    AUTO_FIRED = 9
    AUTO_FIRED_RETURN_NOT_DETECTED = 13
    AUTO_FIRED_RETURN_DETECTED = 15
    NO_FLASH_FUNCTION = 24
    AUTO_NO_FLASH_FUNCTION = 25
    RED_EYE_AUTO_FIRED = 65
    RED_EYE_AUTO_FIRED_RETURN_NOT_DETECTED = 69
    RED_EYE_AUTO_FIRED_RETURN_DETECTED = 71
    RED_EYE_AUTO_NO_FLASH = 73


@dataclass(kw_only=True, slots=True, frozen=True)
class FlashInfo:
    fired: bool
    mode: FlashMode | None = None
    return_light: bool = False
    function_present: bool = False
    red_eye_reduction: bool = False


@dataclass(kw_only=True, slots=True, frozen=True)
class CameraSettings:
    make: str | None = None
    model: str | None = None
    orientation: Orientation | None = None
    focal_length: str | None = None
    focal_length_35mm: str | None = None
    max_aperture: str | None = None
    aperture_value: str | None = None


@dataclass(kw_only=True, slots=True, frozen=True)
class ExposureSettings:
    exposure_time: str | None = None
    aperture: str | None = None
    iso: int | None = None
    exposure_bias: str | None = None
    metering_mode: MeteringMode | None = None
    white_balance: WhiteBalance | None = None


@dataclass(kw_only=True, slots=True, frozen=True)
class GPSInfo:
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    latitude_ref: str | None = None
    longitude_ref: str | None = None


@dataclass(kw_only=True, slots=True, frozen=True)
class DateTimeInfo:
    created: datetime | None = None
    digitized: datetime | None = None
    original: datetime | None = None


@dataclass(eq=False)
class ImageInfo:
    # Basic image properties
    width: int
    height: int
    format: str | None = None
    is_animated: bool = False

    # Structured data
    camera: CameraSettings | None = None
    exposure: ExposureSettings | None = None
    flash: FlashInfo | None = None
    gps: GPSInfo | None = None
    datetime_info: DateTimeInfo | None = None


class ImageInfoExtractor(Protocol):
    @abstractmethod
    async def extract(self, data: bytes) -> ImageInfo: ...
