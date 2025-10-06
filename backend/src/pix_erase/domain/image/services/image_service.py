import logging
from datetime import datetime
from typing import Final, Literal

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.ports.image_color_to_gray_converter import ImageColorToCrayScaleConverter
from pix_erase.domain.image.ports.image_compress_converter import ImageCompressConverter
from pix_erase.domain.image.ports.image_rotation_converter import ImageRotationConverter
from pix_erase.domain.image.ports.image_watermark_remover_converter import ImageWatermarkRemoverConverter
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageService(DomainService):
    def __init__(
            self,
            color_to_gray_converter: ImageColorToCrayScaleConverter,
            compress_converter: ImageCompressConverter,
            rotation_converter: ImageRotationConverter,
            watermark_converter: ImageWatermarkRemoverConverter,
            image_id_generator: ImageIdGenerator,
    ) -> None:
        super().__init__()
        self._color_to_gray_converter: Final[ImageColorToCrayScaleConverter] = color_to_gray_converter
        self._compress_converter: Final[ImageCompressConverter] = compress_converter
        self._rotation_converter: Final[ImageRotationConverter] = rotation_converter
        self._id_generator: Final[ImageIdGenerator] = image_id_generator
        self._watermark_converter: Final[ImageWatermarkRemoverConverter] = watermark_converter

    def create(
            self,
            image_name: ImageName,
            image_height: ImageSize,
            image_width: ImageSize,
            data: bytes,
    ) -> Image:
        logger.debug("Started creating new image in service")
        id_for_image: ImageID = self._id_generator()

        new_image: Image = Image(
            id=id_for_image,
            name=image_name,
            height=image_height,
            width=image_width,
            data=data
        )

        return new_image

    def change_image_name(self, image: Image, new_image_name: ImageName) -> None:
        image.name = new_image_name
        image.updated_at = datetime.now()

    def convert_color_to_gray(self, image: Image) -> None:
        logger.debug("Started converting color to gray, image name: %s", image.name)

        converted_data: bytes = self._color_to_gray_converter.convert(
            data=image.data
        )

        image.data = converted_data
        image.updated_at = datetime.now()

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

    def remove_watermark(self, image: Image) -> None:
        logger.debug("Started removing watermark, image name: %s", image.name)

        converted_data: bytes = self._watermark_converter.convert(
            data=image.data,
        )

        logger.debug("Successfully removed watermark, image name: %s", image.name)

        image.data = converted_data
        image.updated_at = datetime.now()

    def upscale(self, image: Image, algorithm: Literal["AI", "Linear", "Bilinear"]) -> None:
        logger.debug("Started upscaling, image name: %s, algorithm: %s", image.name, algorithm)
        converted_data: bytes

        if algorithm == "Linear":
            ...
        elif algorithm == "Bilinear":
            ...
        elif algorithm == "AI":
            ...
        else:
            ...
