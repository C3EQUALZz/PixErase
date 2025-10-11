import logging
from datetime import datetime
from typing import Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.ports.image_resizer import ImageResizerConverter
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageService(DomainService):
    def __init__(
            self,
            image_id_generator: ImageIdGenerator,
            image_resizer: ImageResizerConverter,
    ) -> None:
        super().__init__()
        self._id_generator: Final[ImageIdGenerator] = image_id_generator
        self._image_resizer: Final[ImageResizerConverter] = image_resizer

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

    def change_image_width(self, image: Image, new_image_width: ImageSize) -> None:
        new_data: bytes = self._image_resizer.resize(
            image.data,
            image_width=new_image_width.value,
            image_height=image.height.value
        )

        image.data = new_data
        image.width = new_image_width
        image.updated_at = datetime.now()

    def change_image_height(self, image: Image, new_image_height: ImageSize) -> None:
        new_data: bytes = self._image_resizer.resize(
            image.data,
            image_width=new_image_height.value,
            image_height=image.height.value
        )

        image.data = new_data
        image.height = new_image_height
        image.updated_at = datetime.now()
