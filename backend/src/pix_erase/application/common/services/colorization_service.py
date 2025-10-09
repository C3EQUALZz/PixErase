import asyncio
from typing import Final

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.errors.image import ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.services.image_service import ImageService
from pix_erase.domain.image.values.image_id import ImageID


class ColorizationService:
    def __init__(
            self,
            file_storage: ImageStorage,
            image_service: ImageService,
    ) -> None:
        self._file_storage: Final[ImageStorage] = file_storage
        self._image_service: Final[ImageService] = image_service

    async def convert_to_grayscale(self, id_for_image: ImageID) -> None:
        image: Image | None = await self._file_storage.read_by_id(
            image_id=id_for_image
        )

        if image is None:
            msg = f"image with id: {id_for_image} not found"
            raise ImageNotFoundError(msg)

        self._image_service.convert_color_to_gray(image=image)

        await self._file_storage.update(image=image)

    async def remove_to_background(self, id_for_image: ImageID) -> None:
        image: Image | None = await self._file_storage.read_by_id(
            image_id=id_for_image
        )

        if image is None:
            msg = f"image with id: {id_for_image} not found"
            raise ImageNotFoundError(msg)

        await asyncio.to_thread(self._image_service.remove_background, image=image)
        await self._file_storage.update(image=image)
