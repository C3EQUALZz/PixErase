import logging
from datetime import datetime
from typing import Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.ports.converter import ImageConverter
from pix_erase.domain.image.ports.factory_converter import FactoryConverter, ImageConverterType
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageService(DomainService):
    def __init__(
            self,
            factory_converter: FactoryConverter,
            image_id_generator: ImageIdGenerator,
    ) -> None:
        super().__init__()
        self._factory_converter: Final[FactoryConverter] = factory_converter
        self._id_generator: Final[ImageIdGenerator] = image_id_generator

    def create(
            self,
            image_name: ImageName,
            image_height: ImageSize,
            image_width: ImageSize,
            data: bytes
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

    def resize(self, image: Image, new_width: ImageSize, new_height: ImageSize) -> None:
        image.width = new_width
        image.height = new_height
        image.updated_at = datetime.now()

    def convert_image(self, image: Image, converter_type: ImageConverterType) -> Image:
        logger.debug("Converting image, converter type %s", converter_type)
        image_converter: ImageConverter = self._factory_converter.create_image_converter(
            image_converter_type=converter_type
        )
        logger.debug("Got image converter: %s", image_converter)
        converted_image: Image = image_converter.convert(image)
        logger.debug("Successfully converted image")
        return converted_image
