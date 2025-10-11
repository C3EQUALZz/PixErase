import logging
from datetime import datetime
from typing import Final, Literal

from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.errors.image import UnknownImageUpscalerError
from pix_erase.domain.image.ports.image_ai_upscaler_converter import ImageAIUpscaleConverter
from pix_erase.domain.image.ports.image_background_remove_converter import ImageRemoveBackgroundConverter
from pix_erase.domain.image.ports.image_color_to_gray_converter import ImageColorToCrayScaleConverter
from pix_erase.domain.image.ports.image_nearest_neighbour_upscale_converter import (
    ImageNearestNeighbourUpscalerConverter
)
from pix_erase.domain.image.ports.image_watermark_remover_converter import ImageWatermarkRemoverConverter
from pix_erase.domain.image.values.image_scale import ImageScale

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageColorizationService:
    def __init__(
            self,
            color_to_gray_converter: ImageColorToCrayScaleConverter,
            image_background_remove_converter: ImageRemoveBackgroundConverter,
            watermark_converter: ImageWatermarkRemoverConverter,
            image_ai_upscale_converter: ImageAIUpscaleConverter,
            image_nearest_upscale_converter: ImageNearestNeighbourUpscalerConverter,
    ) -> None:
        self._colorization_converter: Final[ImageColorToCrayScaleConverter] = color_to_gray_converter
        self._remove_converter: Final[ImageRemoveBackgroundConverter] = image_background_remove_converter
        self._watermark_converter: Final[ImageWatermarkRemoverConverter] = watermark_converter
        self._image_ai_upscale_converter: Final[ImageAIUpscaleConverter] = (
            image_ai_upscale_converter
        )
        self._image_nearest_upscale_converter: Final[ImageNearestNeighbourUpscalerConverter] = (
            image_nearest_upscale_converter
        )

    def convert_color_to_gray(self, image: Image) -> None:
        logger.debug(
            "Started converting color to gray, image name: %s",
            image.name
        )

        converted_data: bytes = self._colorization_converter.convert(data=image.data)
        image.data = converted_data
        image.updated_at = datetime.now()

    def remove_background(self, image: Image) -> None:
        logger.debug(
            "Started removing background, image name: %s",
            image.name,
        )

        converted_data: bytes = self._remove_converter.convert(data=image.data)

        logger.debug("Successfully removed background, image name: %s", image.name)
        image.data = converted_data
        image.updated_at = datetime.now()

    def remove_watermark(self, image: Image) -> None:
        logger.debug("Started removing watermark, image name: %s", image.name)

        converted_data: bytes = self._watermark_converter.convert(data=image.data)

        logger.debug("Successfully removed watermark, image name: %s", image.name)

        image.data = converted_data
        image.updated_at = datetime.now()

    def upscale(
            self,
            image: Image,
            algorithm: Literal["AI", "NearestNeighbour"],
            scale: ImageScale = ImageScale(2)
    ) -> None:
        logger.debug("Started upscaling, image name: %s, algorithm: %s", image.name, algorithm)
        converted_data: bytes

        if algorithm == "NearestNeighbour":
            converted_data = self._image_nearest_upscale_converter.convert(
                data=image.data,
                width=image.width.value,
                height=image.height.value,
                scale=scale
            )
        elif algorithm == "AI":
            converted_data = self._image_ai_upscale_converter.convert(
                data=image.data,
                width=image.width.value,
                height=image.height.value,
                scale=scale
            )
        else:
            msg = "Unknown algorithm for upscaling."
            raise UnknownImageUpscalerError(msg)

        image.data = converted_data
        image.updated_at = datetime.now()
