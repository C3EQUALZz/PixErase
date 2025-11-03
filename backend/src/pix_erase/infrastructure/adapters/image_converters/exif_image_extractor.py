import logging
from datetime import datetime
from typing import override, Final, Any, Mapping, Literal, MutableMapping, cast

import cv2
import exif
import numpy as np
from exif import Image

from pix_erase.application.common.ports.image.extractor import (
    ImageInfoExtractor,
    ImageInfo,
    GPSInfo,
    FlashInfo,
    ExposureSettings,
    CameraSettings,
    DateTimeInfo,
    Orientation,
    MeteringMode,
    WhiteBalance,
    FlashMode
)
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ExifImageInfoExtractor(ImageInfoExtractor):
    @override
    async def extract(self, data: bytes) -> ImageInfo:
        # Декодируем изображение для получения размеров
        buffer = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

        if img is None:
            raise ImageDecodingError("Failed to decode image")

        height, width, _ = img.shape

        # Извлекаем EXIF данные
        exif_data = self._safe_extract_exif(data)

        # Определяем формат и анимацию
        format_type = self._detect_format(data)
        is_animated = self._check_if_animated(data)

        # Создаем структурированные объекты
        camera_settings = self._create_camera_settings(exif_data)
        exposure_settings = self._create_exposure_settings(exif_data)
        flash_info = self._create_flash_info(exif_data)
        gps_info = self._create_gps_info(exif_data)
        datetime_info = self._create_datetime_info(exif_data)

        return ImageInfo(
            width=width,
            height=height,
            format=format_type,
            is_animated=is_animated,
            camera=camera_settings,
            exposure=exposure_settings,
            flash=flash_info,
            gps=gps_info,
            datetime_info=datetime_info
        )

    @staticmethod
    def _safe_extract_exif(data: bytes) -> Mapping[str, Any]:
        """Безопасно извлекает EXIF данные"""
        exif_data: MutableMapping[str, Any] = {}

        try:
            pic = Image(data)
            if not pic.has_exif:
                return exif_data

            attributes = [
                "model", "orientation", "datetime", "make", "f_number",
                "exposure_time", "focal_length", "flash", "metering_mode",
                "photographic_sensitivity", "focal_length_in_35mm_film",
                "max_aperture_value", "datetime_digitized", "exposure_bias_value",
                "white_balance", "datetime_original", "aperture_value",
                "gps_latitude_ref", "gps_latitude", "gps_longitude", "gps_longitude_ref"
            ]

            for attr in attributes:
                try:
                    value = getattr(pic, attr, None)
                    if value is not None:
                        exif_data[attr] = value
                except AttributeError:
                    continue

        except Exception as e:
            logger.warning("Failed to extract EXIF data: %s", e)

        return cast(Mapping[str, Any], exif_data)

    def _create_camera_settings(self, exif_data: Mapping[str, Any]) -> CameraSettings | None:
        if not any([exif_data.get('make'), exif_data.get('model')]):
            return None

        return CameraSettings(
            make=self._format_camera_make(exif_data.get('make')),
            model=self._format_camera_model(exif_data.get('model')),
            orientation=self._parse_orientation(exif_data.get('orientation')),
            focal_length=self._format_focal_length(exif_data.get('focal_length')),
            focal_length_35mm=self._format_focal_length(exif_data.get('focal_length_in_35mm_film')),
            max_aperture=self._format_aperture(exif_data.get('max_aperture_value')),
            aperture_value=self._format_aperture(exif_data.get('aperture_value'))
        )

    def _create_exposure_settings(self, exif_data: Mapping[str, Any]) -> ExposureSettings | None:
        if not any([
            exif_data.get('exposure_time'), exif_data.get('f_number'),
            exif_data.get('photographic_sensitivity')
        ]):
            return None

        return ExposureSettings(
            exposure_time=self._format_exposure_time(exif_data.get('exposure_time')),
            aperture=self._format_aperture(exif_data.get('f_number')),
            iso=exif_data.get('photographic_sensitivity'),
            exposure_bias=self._format_exposure_bias(exif_data.get('exposure_bias_value')),
            metering_mode=self._parse_metering_mode(exif_data.get('metering_mode')),
            white_balance=self._parse_white_balance(exif_data.get('white_balance'))
        )

    def _create_flash_info(self, exif_data: Mapping[str, Any]) -> FlashInfo | None:
        flash = exif_data.get('flash')
        if not flash:
            return None

        return FlashInfo(
            fired=getattr(flash, 'flash_fired', False),
            mode=self._parse_flash_mode(flash),
            return_light=getattr(flash, 'flash_return', False),
            function_present=not getattr(flash, 'flash_function_not_present', True),
            red_eye_reduction=getattr(flash, 'red_eye_reduction_supported', False)
        )

    def _create_gps_info(self, exif_data: Mapping[str, Any]) -> GPSInfo | None:
        latitude = exif_data.get('gps_latitude')
        longitude = exif_data.get('gps_longitude')

        if not latitude or not longitude:
            return None

        lat_decimal, lon_decimal = self._convert_gps_to_decimal(
            latitude, longitude,
            exif_data.get('gps_latitude_ref', 'N'),
            exif_data.get('gps_longitude_ref', 'E')
        )

        return GPSInfo(
            latitude=lat_decimal,
            longitude=lon_decimal,
            latitude_ref=exif_data.get('gps_latitude_ref'),
            longitude_ref=exif_data.get('gps_longitude_ref')
        )

    def _create_datetime_info(self, exif_data: Mapping[str, Any]) -> DateTimeInfo | None:
        return DateTimeInfo(
            created=self._parse_datetime(exif_data.get('datetime')),
            digitized=self._parse_datetime(exif_data.get('datetime_digitized')),
            original=self._parse_datetime(exif_data.get('datetime_original'))
        )

    @staticmethod
    def _parse_orientation(orientation: exif.Orientation | None) -> Orientation | None:
        if orientation is None:
            return None
        try:
            return Orientation(orientation.value if hasattr(orientation, 'value') else orientation)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_metering_mode(metering_mode: exif.MeteringMode | None) -> MeteringMode | None:
        if metering_mode is None:
            return None
        try:
            return MeteringMode(metering_mode.value if hasattr(metering_mode, 'value') else metering_mode)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_white_balance(white_balance: exif.WhiteBalance | None) -> WhiteBalance | None:
        if white_balance is None:
            return None
        try:
            return WhiteBalance(white_balance.value if hasattr(white_balance, 'value') else white_balance)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_flash_mode(flash: exif.Flash | None) -> FlashMode | None:
        if not flash:
            return None
        try:
            # Создаем битовую маску для определения режима вспышки
            mode_value = 0
            if getattr(flash, 'flash_fired', False):
                mode_value |= 1
            if getattr(flash, 'flash_return', 0):
                mode_value |= 4
            if getattr(flash, 'flash_mode', 0):
                mode_value |= 24
            if getattr(flash, 'red_eye_reduction_supported', False):
                mode_value |= 64

            return FlashMode(mode_value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _detect_format(data: bytes) -> Literal["JPEG", "PNG", "GIF", "WEBP", "UNKNOWN"]:
        """Определяет формат изображения по сигнатурам"""
        if data.startswith(b'\xff\xd8\xff'):
            return "JPEG"

        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            return "PNG"

        if data.startswith(b'GIF8'):
            return "GIF"

        if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            return "WEBP"

        return "UNKNOWN"

    @staticmethod
    def _format_camera_make(data: str | None) -> str | None:
        if data is None:
            return None
        return data.strip()

    @staticmethod
    def _format_camera_model(data: str | None) -> str | None:
        if data is None:
            return None
        return data.strip()

    def _check_if_animated(self, data: bytes) -> bool:
        """Проверяет, является ли изображение анимированным"""
        format_type = self._detect_format(data)

        if format_type == "GIF":
            return data.count(b'\x21\xF9\x04') > 1
        elif format_type == "PNG":
            return b'acTL' in data
        elif format_type == "WEBP":
            return b'ANIM' in data

        return False

    @staticmethod
    def _format_exposure_time(value: tuple[int, int] | float | None | object) -> str | None:
        if value is None:
            return None
        try:
            if isinstance(value, tuple) and len(value) == 2:
                numerator, denominator = value
                if denominator == 1:
                    return f"{numerator}s"
                return f"{numerator}/{denominator}s"
            if isinstance(value, float):
                # Для десятичных значений (например, 0.0125)
                from fractions import Fraction
                frac = Fraction(value).limit_denominator(1000)
                return f"{frac.numerator}/{frac.denominator}s"
            return str(value)
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_aperture(value: str | None) -> str | None:
        if value is None:
            return None
        try:
            return f"f/{float(value):.1f}"
        except (TypeError, ValueError):
            return str(value) if value else None

    @staticmethod
    def _format_focal_length(value: str | None) -> str | None:
        if value is None:
            return None
        try:
            return f"{float(value)}mm"
        except (TypeError, ValueError):
            return str(value) if value else None

    @staticmethod
    def _format_exposure_bias(value: str | None) -> str | None:
        if value is None:
            return None
        try:
            return f"{float(value):+.1f} EV"
        except (TypeError, ValueError):
            return str(value) if value else None

    @staticmethod
    def _parse_datetime(datetime_str: str | None) -> datetime | None:
        if not datetime_str:
            return None
        try:
            return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _convert_gps_to_decimal(
            latitude: tuple[float, float, float],
            longitude: tuple[float, float, float],
            lat_ref: str,
            lon_ref: str
    ) -> tuple[float, float]:
        """
        Конвертирует GPS координаты из формата (degrees, minutes, seconds) в десятичные градусы

        Args:
            latitude: Кортеж (degrees, minutes, seconds) для широты
            longitude: Кортеж (degrees, minutes, seconds) для долготы
            lat_ref: Референс широты ('N' или 'S')
            lon_ref: Референс долготы ('E' или 'W')

        Returns:
            tuple[float, float]: (широта в десятичных градусах, долгота в десятичных градусах)
        """

        def convert_single_coord(coord: tuple, ref: str) -> float:
            """
            Конвертирует одну координату в десятичный формат
            """
            try:
                if isinstance(coord, tuple) and len(coord) == 3:
                    degrees, minutes, seconds = coord

                    # Если значения являются дробями (кортежами), конвертируем их в float
                    if isinstance(degrees, tuple):
                        degrees = degrees[0] / degrees[1] if degrees[1] != 0 else 0
                    if isinstance(minutes, tuple):
                        minutes = minutes[0] / minutes[1] if minutes[1] != 0 else 0
                    if isinstance(seconds, tuple):
                        seconds = seconds[0] / seconds[1] if seconds[1] != 0 else 0

                    # Преобразуем в десятичный формат
                    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600

                    # Учитываем направление (N/S, E/W)
                    if ref in ['S', 'W']:
                        decimal = -decimal

                    return decimal
                else:
                    # Если координата уже в неправильном формате, пытаемся преобразовать как есть
                    return float(coord) # type: ignore
            except (TypeError, ValueError, ZeroDivisionError) as e:
                logger.warning(f"Failed to convert GPS coordinate {coord}: {e}")
                return 0.0

        lat_decimal = convert_single_coord(latitude, lat_ref)
        lon_decimal = convert_single_coord(longitude, lon_ref)

        return lat_decimal, lon_decimal

