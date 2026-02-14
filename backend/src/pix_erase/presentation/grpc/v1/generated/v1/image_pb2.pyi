from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateImageRequest(_message.Message):
    __slots__ = ("image_data", "filename")
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    image_data: bytes
    filename: str
    def __init__(self, image_data: _Optional[bytes] = ..., filename: _Optional[str] = ...) -> None: ...

class CreateImageResponse(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class ReadImageRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class ReadImageChunk(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class DeleteImageRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class ReadImageExifRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class CameraSettingsExif(_message.Message):
    __slots__ = ("make", "model", "orientation", "focal_length", "focal_length_35mm", "max_aperture", "aperture_value")
    MAKE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    FOCAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    FOCAL_LENGTH_35MM_FIELD_NUMBER: _ClassVar[int]
    MAX_APERTURE_FIELD_NUMBER: _ClassVar[int]
    APERTURE_VALUE_FIELD_NUMBER: _ClassVar[int]
    make: str
    model: str
    orientation: str
    focal_length: str
    focal_length_35mm: str
    max_aperture: str
    aperture_value: str
    def __init__(self, make: _Optional[str] = ..., model: _Optional[str] = ..., orientation: _Optional[str] = ..., focal_length: _Optional[str] = ..., focal_length_35mm: _Optional[str] = ..., max_aperture: _Optional[str] = ..., aperture_value: _Optional[str] = ...) -> None: ...

class ExposureSettings(_message.Message):
    __slots__ = ("exposure_time", "aperture", "iso", "exposure_bias", "metering_mode", "white_balance")
    EXPOSURE_TIME_FIELD_NUMBER: _ClassVar[int]
    APERTURE_FIELD_NUMBER: _ClassVar[int]
    ISO_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_BIAS_FIELD_NUMBER: _ClassVar[int]
    METERING_MODE_FIELD_NUMBER: _ClassVar[int]
    WHITE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    exposure_time: str
    aperture: str
    iso: int
    exposure_bias: str
    metering_mode: str
    white_balance: str
    def __init__(self, exposure_time: _Optional[str] = ..., aperture: _Optional[str] = ..., iso: _Optional[int] = ..., exposure_bias: _Optional[str] = ..., metering_mode: _Optional[str] = ..., white_balance: _Optional[str] = ...) -> None: ...

class FlashInfo(_message.Message):
    __slots__ = ("fired", "mode", "return_light", "function_present", "red_eye_reduction")
    FIRED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    RETURN_LIGHT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_PRESENT_FIELD_NUMBER: _ClassVar[int]
    RED_EYE_REDUCTION_FIELD_NUMBER: _ClassVar[int]
    fired: bool
    mode: str
    return_light: bool
    function_present: bool
    red_eye_reduction: bool
    def __init__(self, fired: bool = ..., mode: _Optional[str] = ..., return_light: bool = ..., function_present: bool = ..., red_eye_reduction: bool = ...) -> None: ...

class GPSInfo(_message.Message):
    __slots__ = ("latitude", "longitude", "altitude", "latitude_ref", "longitude_ref")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_REF_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_REF_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    altitude: float
    latitude_ref: str
    longitude_ref: str
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., latitude_ref: _Optional[str] = ..., longitude_ref: _Optional[str] = ...) -> None: ...

class DateTimeInfo(_message.Message):
    __slots__ = ("created", "digitized", "original")
    CREATED_FIELD_NUMBER: _ClassVar[int]
    DIGITIZED_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_FIELD_NUMBER: _ClassVar[int]
    created: str
    digitized: str
    original: str
    def __init__(self, created: _Optional[str] = ..., digitized: _Optional[str] = ..., original: _Optional[str] = ...) -> None: ...

class ReadImageExifResponse(_message.Message):
    __slots__ = ("width", "height", "format", "is_animated", "camera_settings", "exposure_settings", "flash_info", "gps_info", "datetime_info")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    IS_ANIMATED_FIELD_NUMBER: _ClassVar[int]
    CAMERA_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FLASH_INFO_FIELD_NUMBER: _ClassVar[int]
    GPS_INFO_FIELD_NUMBER: _ClassVar[int]
    DATETIME_INFO_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    format: str
    is_animated: bool
    camera_settings: CameraSettingsExif
    exposure_settings: ExposureSettings
    flash_info: FlashInfo
    gps_info: GPSInfo
    datetime_info: DateTimeInfo
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., format: _Optional[str] = ..., is_animated: bool = ..., camera_settings: _Optional[_Union[CameraSettingsExif, _Mapping]] = ..., exposure_settings: _Optional[_Union[ExposureSettings, _Mapping]] = ..., flash_info: _Optional[_Union[FlashInfo, _Mapping]] = ..., gps_info: _Optional[_Union[GPSInfo, _Mapping]] = ..., datetime_info: _Optional[_Union[DateTimeInfo, _Mapping]] = ...) -> None: ...

class CompressImageRequest(_message.Message):
    __slots__ = ("image_id", "quality")
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    quality: int
    def __init__(self, image_id: _Optional[str] = ..., quality: _Optional[int] = ...) -> None: ...

class GrayscaleImageRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class RemoveBackgroundRequest(_message.Message):
    __slots__ = ("image_id",)
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    def __init__(self, image_id: _Optional[str] = ...) -> None: ...

class RotateImageRequest(_message.Message):
    __slots__ = ("image_id", "angle")
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    angle: int
    def __init__(self, image_id: _Optional[str] = ..., angle: _Optional[int] = ...) -> None: ...

class UpscaleImageRequest(_message.Message):
    __slots__ = ("image_id", "algorithm", "scale")
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    image_id: str
    algorithm: str
    scale: int
    def __init__(self, image_id: _Optional[str] = ..., algorithm: _Optional[str] = ..., scale: _Optional[int] = ...) -> None: ...

class TaskResponse(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...
