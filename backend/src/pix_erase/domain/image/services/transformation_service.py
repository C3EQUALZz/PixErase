import logging
from datetime import datetime
from typing import Final

from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.ports.image_compress_converter import ImageCompressConverter
from pix_erase.domain.image.ports.image_rotation_converter import ImageRotationConverter

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageTransformationService:
    def __init__(
            self,
            compress_converter: ImageCompressConverter,
            rotation_converter: ImageRotationConverter,
    ) -> None:
        self._compress_converter: Final[ImageCompressConverter] = compress_converter
        self._rotation_converter: Final[ImageRotationConverter] = rotation_converter

    def compress_image(self, image: Image, quality: int = 90) -> None:
        logger.debug("Started compressing image, image name: %s", image.name)

        converted_data: bytes = self._compress_converter.convert(
            data=image.data,
            quality=quality
        )

        logger.debug("Successfully compressed image, image name: %s", image.name)

        image.data = converted_data
        image.updated_at = datetime.now()

    def rotate_image(self, image: Image, angle: int = 90) -> None:
        logger.debug("Started rotating image, image name: %s", image.name)

        converted_data: bytes = self._rotation_converter.convert(
            data=image.data,
            angle=angle
        )

        logger.debug("Successfully rotated image, image name: %s", image.name)

        image.data = converted_data
        image.updated_at = datetime.now()
