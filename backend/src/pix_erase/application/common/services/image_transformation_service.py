from typing import Final

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.errors.image import ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.services.image_service import ImageService
from pix_erase.domain.image.values.image_id import ImageID


class ImageTransformationService:
    def __init__(
            self,
            file_storage: ImageStorage,
            image_service: ImageService,
    ) -> None:
        self._file_storage: Final[ImageStorage] = file_storage
        self._image_service: Final[ImageService] = image_service

    async def rotate_image(self, id_for_image: ImageID, angle: int = 90) -> None:
        image: Image | None = await self._file_storage.read_by_id(
            image_id=id_for_image
        )

        if image is None:
            msg = f"image with id: {id_for_image} not found"
            raise ImageNotFoundError(msg)

        self._image_service.rotate_image(image=image, angle=angle)

        await self._file_storage.update(image=image)

    async def compress_image(self, id_for_image: ImageID, quality: int = 90) -> None:
        image: Image | None = await self._file_storage.read_by_id(
            image_id=id_for_image
        )

        if image is None:
            msg = f"image with id: {id_for_image} not found"
            raise ImageNotFoundError(msg)

        self._image_service.compress_image(image=image, quality=quality)

        await self._file_storage.update(image=image)
