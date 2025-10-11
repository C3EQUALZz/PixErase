import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CompareImageCommand:
    first_image: UUID
    second_image: UUID


@final
class CompareImageCommandHandler:
    def __init__(
            self,
            current_user_service: CurrentUserService,
            image_storage: ImageStorage,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._image_storage: Final[ImageStorage] = image_storage

    async def __call__(self, data: CompareImageCommand):
        logger.info(
            "Started comparing images. First image id: %s, second image id: %s",
            data.first_image,
            data.second_image,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        typed_first_image_id: ImageID = ImageID(data.first_image)
        typed_second_image_id: ImageID = ImageID(data.second_image)

        if typed_first_image_id not in current_user.images:
            msg = f"Image with id: {data.first_image} doesnt belong to this user."
            raise ImageDoesntBelongToThisUserError(msg)

        if typed_second_image_id not in current_user.images:
            msg = f"Image with id: {data.second_image} doesnt belong to this user."
            raise ImageDoesntBelongToThisUserError(msg)

        first_image: Image | None = await self._image_storage.read_by_id(image_id=typed_first_image_id)

        if first_image is None:
            msg = f"Failed to found image with id: {data.first_image}"
            raise ImageNotFoundError(msg)

        second_image: Image | None = await self._image_storage.read_by_id(image_id=typed_second_image_id)

        if second_image is None:
            msg = f"Failed to found image with id: {data.second_image}"
            raise ImageNotFoundError(msg)

        different_names: bool = first_image.name != second_image.name
        different_width: bool = first_image.width != second_image.width
        different_height: bool = first_image.height != second_image.height


