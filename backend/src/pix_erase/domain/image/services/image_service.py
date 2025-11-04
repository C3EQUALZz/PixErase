import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.ports.image_comparer_converter import ImageComparerConverter
from pix_erase.domain.image.ports.image_resizer import ImageResizerConverter
from pix_erase.domain.image.services.contracts import ImageComparisonResult
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize

if TYPE_CHECKING:
    from pix_erase.domain.image.values.image_id import ImageID

logger: Final[logging.Logger] = logging.getLogger(__name__)


class ImageService(DomainService):
    def __init__(
        self,
        image_id_generator: ImageIdGenerator,
        image_resizer: ImageResizerConverter,
        image_comparer: ImageComparerConverter,
    ) -> None:
        super().__init__()
        self._id_generator: Final[ImageIdGenerator] = image_id_generator
        self._image_resizer: Final[ImageResizerConverter] = image_resizer
        self._image_comparer: Final[ImageComparerConverter] = image_comparer

    def create(
        self,
        image_name: ImageName,
        image_height: ImageSize,
        image_width: ImageSize,
        data: bytes,
    ) -> Image:
        logger.debug("Started creating new image in service")
        id_for_image: ImageID = self._id_generator()

        new_image: Image = Image(id=id_for_image, name=image_name, height=image_height, width=image_width, data=data)

        return new_image

    def change_image_name(self, image: Image, new_image_name: ImageName) -> None:
        image.name = new_image_name
        image.updated_at = datetime.now(UTC)

    def change_image_width(self, image: Image, new_image_width: ImageSize) -> None:
        new_data: bytes = self._image_resizer.resize(
            image.data, image_width=new_image_width.value, image_height=image.height.value
        )

        image.data = new_data
        image.width = new_image_width
        image.updated_at = datetime.now(UTC)

    def change_image_height(self, image: Image, new_image_height: ImageSize) -> None:
        new_data: bytes = self._image_resizer.resize(
            image.data, image_width=new_image_height.value, image_height=image.height.value
        )

        image.data = new_data
        image.height = new_image_height
        image.updated_at = datetime.now(UTC)

    def compare_images(self, first_image: Image, second_image: Image) -> ImageComparisonResult:
        """
        Compare two images using histogram and similarity metrics.

        Returns comparison scores and metadata differences.
        """
        logger.debug("Started comparing images: %s and %s", first_image.id, second_image.id)

        scores = self._image_comparer.compare_by_histograms(
            first_image=first_image.data,
            second_image=second_image.data,
        )
        logger.debug("Successfully calculated comparison scores")

        different_names: bool = first_image.name != second_image.name
        different_width: bool = first_image.width != second_image.width
        different_height: bool = first_image.height != second_image.height

        logger.debug(
            "Image comparison completed. Names differ: %s, Width differs: %s, Height differs: %s",
            different_names,
            different_width,
            different_height,
        )

        return ImageComparisonResult(
            scores=scores,
            different_names=different_names,
            different_width=different_width,
            different_height=different_height,
        )
