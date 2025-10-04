import io
import logging
from datetime import datetime
from typing import override, Final, Any, MutableMapping

from PIL import Image, ExifTags

from pix_erase.application.common.ports.image.extractor import ImageInfoExtractor, ImageInfo

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ExifImageInfoExtractor(ImageInfoExtractor):
    @override
    async def extract(self, data: bytes) -> ImageInfo:
        with Image.open(io.BytesIO(data)) as img:
            width, height = img.size
            is_animated = getattr(img, "is_animated", False)

            img_exif = img.getexif()

            if not img_exif:
                logger.info("No EXIF data found in image")
                return ImageInfo(
                    width=width,
                    height=height,
                    format=img.format,
                    is_animated=is_animated,
                    camera_make=None,
                    camera_model=None,
                    exposure_time=None,
                    aperture=None,
                    focal_length=None,
                    iso=None,
                    created_date=None,
                    gps_info=None,
                )

            exif_data: MutableMapping[str, Any] = {}
            for tag_id, value in img_exif.items():
                tag_name: str = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag_name] = value

            # Извлекаем и форматируем специфические поля
            return ImageInfo(
                width=width,
                height=height,
                format=img.format,
                is_animated=is_animated,
                camera_make=exif_data.get('Make'),
                camera_model=exif_data.get('Model'),
                exposure_time=self._format_exposure_time(exif_data.get('ExposureTime')),
                aperture=self._format_aperture(exif_data.get('FNumber')),
                focal_length=self._format_focal_length(exif_data.get('FocalLength')),
                iso=exif_data.get('ISOSpeedRatings'),
                created_date=self._parse_datetime(exif_data.get('DateTime')),
                gps_info=exif_data.get('GPSInfo'),
            )

    @staticmethod
    def _format_exposure_time(value: str | tuple[str, str] | None) -> str | None:
        """Форматирует время экспозиции в читаемый вид"""
        if value is None:
            return None
        try:
            if isinstance(value, tuple) and len(value) == 2:
                numerator, denominator = value
                if denominator == 1:
                    return f"{numerator}s"
                return f"{numerator}/{denominator}s"
            return str(value)
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_aperture(value: str | tuple[str, str] | None) -> str | None:
        """Форматирует значение диафрагмы"""
        if value is None:
            return None
        try:
            if isinstance(value, tuple) and len(value) == 2:
                aperture_value = float(value[0]) / float(value[1])
                return f"f/{aperture_value:.1f}"
            return f"f/{float(value):.1f}"
        except (TypeError, ValueError, ZeroDivisionError):
            return str(value) if value else None

    @staticmethod
    def _format_focal_length(value: str | tuple[str, str] | None) -> str | None:
        """Форматирует фокусное расстояние"""
        if value is None:
            return None
        try:
            if isinstance(value, tuple) and len(value) == 2:
                focal_length = float(value[0]) / float(value[1])
                return f"{focal_length:.1f}mm"
            return f"{float(value)}mm"
        except (TypeError, ValueError, ZeroDivisionError):
            return str(value) if value else None

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        """Парсит дату и время из EXIF"""
        if not value:
            return None
        try:
            # EXIF datetime формат: "YYYY:MM:DD HH:MM:SS"
            return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        except (ValueError, TypeError) as e:
            logger.debug(f"Failed to parse datetime '{value}': {e}")
            return None
