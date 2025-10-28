from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, ConfigDict

from pix_erase.application.common.views.image.read_image import (
    CameraOrientationView,
    MeteringModeView,
    WhiteBalanceView,
    FlashModeView
)


class CameraSettingsSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    make: Annotated[
        str,
        Field(
            description="Производитель камеры",
            examples=["Canon", "Nikon", "Sony"],
            max_length=50
        )
    ]
    model: Annotated[
        str,
        Field(
            description="Модель камеры",
            examples=["EOS R5", "D850", "Alpha 7 IV"],
            max_length=50
        )
    ]
    orientation: Annotated[
        CameraOrientationView,
        Field(description="Ориентация камеры при съемке")
    ]
    focal_length: Annotated[
        str,
        Field(
            description="Фокусное расстояние объектива",
            examples=["50.0 mm", "24-70 mm"],
            max_length=20
        )
    ]
    focal_length_35mm: Annotated[
        str,
        Field(
            description="Эквивалентное фокусное расстояние для 35mm плёнки",
            examples=["75.0 mm", "36-105 mm"],
            max_length=20
        )
    ]
    max_aperture: Annotated[
        str,
        Field(
            description="Максимальная диафрагма объектива",
            examples=["f/2.8", "f/1.4"],
            max_length=10,
            pattern=r'^f/[0-9]+(\.[0-9]+)?$'
        )
    ]
    aperture_value: Annotated[
        str,
        Field(
            description="Значение диафрагмы при съёмке",
            examples=["f/5.6", "f/8.0"],
            max_length=10,
            pattern=r'^f/[0-9]+(\.[0-9]+)?$'
        )
    ]


class ExposureSettingsSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    exposure_time: Annotated[
        str,
        Field(
            description="Время выдержки в секундах",
            examples=["1/125", "1.3", "30"],
            max_length=15
        )
    ]
    aperture: Annotated[
        str,
        Field(
            description="Диафрагма",
            examples=["f/5.6", "f/8"],
            max_length=10,
            pattern=r'^f/[0-9]+(\.[0-9]+)?$'
        )
    ]
    iso: Annotated[
        int,
        Field(
            description="Чувствительность ISO",
            ge=1,
            le=51200,
            examples=[100, 400, 3200]
        )
    ]
    exposure_bias: Annotated[
        str,
        Field(
            description="Коррекция экспозиции в EV",
            examples=["0 EV", "-1.3 EV", "+2 EV"],
            max_length=10
        )
    ]
    metering_mode: Annotated[
        MeteringModeView,
        Field(description="Режим замера экспозиции")
    ]
    white_balance: Annotated[
        WhiteBalanceView,
        Field(description="Баланс белого")
    ]


class FlashInfoSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    fired: Annotated[
        bool,
        Field(description="Сработала ли вспышка")
    ]
    mode: Annotated[
        FlashModeView,
        Field(description="Режим работы вспышки")
    ]
    return_light: Annotated[
        bool,
        Field(description="Был ли обнаружен отражённый свет")
    ]
    function_present: Annotated[
        bool,
        Field(description="Наличие функции вспышки")
    ]
    red_eye_reduction: Annotated[
        bool,
        Field(description="Был ли включен режим уменьшения красных глаз")
    ]


class GPSInfoSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    latitude: Annotated[
        float,
        Field(
            description="Географическая широта в градусах",
            ge=-90.0,
            le=90.0,
            examples=[55.7558, 37.6173]
        )
    ]
    longitude: Annotated[
        float,
        Field(
            description="Географическая долгота в градусах",
            ge=-180.0,
            le=180.0,
            examples=[37.6173, -122.4194]
        )
    ]
    altitude: Annotated[
        float,
        Field(
            description="Высота над уровнем моря в метрах",
            examples=[150.5, -50.0]
        )
    ]
    latitude_ref: Annotated[
        Literal["N", "S", "unknown"],
        Field(
            description="Референс широты (N - север, S - юг)",
            examples=["N", "S", "unknown"],
        )
    ]
    longitude_ref: Annotated[
        Literal["E", "W", "unknown"],
        Field(
            description="Референс долготы (E - восток, W - запад)",
            examples=["E", "W"],
        )
    ]


class DateTimeInfoSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    created: Annotated[
        datetime,
        Field(
            description="Дата и время создания файла",
            examples=["2023-12-01T10:30:00"]
        )
    ]
    digitized: Annotated[
        datetime,
        Field(
            description="Дата и время оцифровки",
            examples=["2023-12-01T10:30:00"]
        )
    ]
    original: Annotated[
        datetime,
        Field(
            description="Оригинальная дата и время съёмки",
            examples=["2023-12-01T10:30:00"]
        )
    ]


class ReadImageExifSchemaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    width: Annotated[
        int,
        Field(
            description="Ширина изображения в пикселях",
            ge=1,
            le=30000,
            examples=[1920, 4000, 6000]
        )
    ]
    height: Annotated[
        int,
        Field(
            description="Высота изображения в пикселях",
            ge=1,
            le=30000,
            examples=[1080, 3000, 4000]
        )
    ]
    format: Annotated[
        str,
        Field(
            description="Формат изображения",
            examples=["JPEG", "PNG", "HEIC", "WEBP"],
            max_length=10
        )
    ]
    is_animated: Annotated[
        bool,
        Field(description="Является ли изображение анимированным")
    ]

    camera_settings: Annotated[
        CameraSettingsSchemaResponse,
        Field(description="Настройки камеры")
    ]
    exposure_settings: Annotated[
        ExposureSettingsSchemaResponse,
        Field(description="Настройки экспозиции")
    ]
    flash_info: Annotated[
        FlashInfoSchemaResponse,
        Field(description="Информация о вспышке")
    ]
    gps_info: Annotated[
        GPSInfoSchemaResponse,
        Field(description="Географические координаты")
    ]
    datetime_info: Annotated[
        DateTimeInfoSchemaResponse,
        Field(description="Географические координаты")
    ]
