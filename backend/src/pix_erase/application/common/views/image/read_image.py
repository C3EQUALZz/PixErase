from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadImageByIDView:
    data: AsyncGenerator[bytes, None]
    name: str
    height: int
    width: int
    content_type: str
    content_length: int
    etag: str | None
    created_at: datetime
    updated_at: datetime


class CameraOrientationView(StrEnum):
    UNKNOWN = "unknown"
    TOP_LEFT = "top left"
    TOP_RIGHT = "top right"
    BOTTOM_RIGHT = "bottom right"
    BOTTOM_LEFT = "bottom left"
    LEFT_TOP = "left top"
    RIGHT_TOP = "right top"
    RIGHT_BOTTOM = "right bottom"
    LEFT_BOTTOM = "left bottom"


class MeteringModeView(StrEnum):
    UNKNOWN = "unknown"
    AVERAGE = "average"
    CENTER_WEIGHTED_AVERAGE = "center weighted average"
    SPOT = "spot"
    MULTI_SPOT = "multi spot"
    PATTERN = "pattern"
    PARTIAL = "partial"
    OTHER = "other"


class WhiteBalanceView(StrEnum):
    UNKNOWN = "unknown"
    AUTO = "auto"
    MANUAL = "manual"


class FlashModeView(StrEnum):
    UNKNOWN = "unknown"
    NO_FLASH = "no flash"
    FIRED = "fired"
    FIRED_RETURN_NOT_DETECTED = "fired return not detected"
    FIRED_RETURN_DETECTED = "fired return detected"
    AUTO_NO_FLASH = "auto no flash"
    AUTO_FIRED = "auto fired"
    AUTO_FIRED_RETURN_NOT_DETECTED = "auto fired return not detected"
    AUTO_FIRED_RETURN_DETECTED = "auto fired return detected"
    NO_FLASH_FUNCTION = "no flash function"
    AUTO_NO_FLASH_FUNCTION = "auto no flash function"
    RED_EYE_AUTO_FIRED = "red eye auto-fired"
    RED_EYE_AUTO_FIRED_RETURN_NOT_DETECTED = "red eye auto-fired return not detected"
    RED_EYE_AUTO_FIRED_RETURN_DETECTED = "red eye auto-fired detected"
    RED_EYE_AUTO_NO_FLASH = "red eye auto-no flash"


@dataclass(frozen=True, slots=True, kw_only=True)
class CameraSettingsExifView:
    make: str
    model: str
    orientation: CameraOrientationView
    focal_length: str
    focal_length_35mm: str
    max_aperture: str
    aperture_value: str


@dataclass(kw_only=True, slots=True, frozen=True)
class ExposureSettingsView:
    exposure_time: str
    aperture: str
    iso: int
    exposure_bias: str
    metering_mode: MeteringModeView
    white_balance: WhiteBalanceView


@dataclass(kw_only=True, slots=True, frozen=True)
class FlashInfoView:
    fired: bool
    mode: FlashModeView
    return_light: bool
    function_present: bool
    red_eye_reduction: bool


@dataclass(kw_only=True, slots=True, frozen=True)
class GPSInfoView:
    latitude: float
    longitude: float
    altitude: float
    latitude_ref: str
    longitude_ref: str


@dataclass(kw_only=True, slots=True, frozen=True)
class DateTimeInfoView:
    created: datetime
    digitized: datetime
    original: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadImageExifView:
    width: int
    height: int
    format: str
    is_animated: bool

    camera_settings: CameraSettingsExifView
    exposure_settings: ExposureSettingsView
    flash_info: FlashInfoView
    gps_info: GPSInfoView
    datetime_info: DateTimeInfoView
