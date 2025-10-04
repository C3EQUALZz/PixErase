import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.image.task_manager import ImageTaskManager
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RotateImageCommand:
    image_id: UUID
    angle: int


@final
class RotateImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Changes existing image.
    """
    def __init__(
            self,
            image_storage: ImageStorage,
            task_manager: ImageTaskManager,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._task_manager: Final[ImageTaskManager] = task_manager
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: RotateImageCommand) -> None:
        logger.info(
            "Started rotating image with id: %s and angle: %d",
            data.image_id,
            data.angle,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        typed_image_id: ImageID = cast(ImageID, data.image_id)

        if typed_image_id not in current_user.images:
            msg = f"Image with id: {data.image_id} doesnt belong to this user."
            raise ImageDoesntBelongToThisUserError(msg)

        image: Image | None = await self._image_storage.read_by_id(image_id=typed_image_id)

        if image is None:
            msg = f"Failed to found image with id: {data.image_id}"
            raise ImageNotFoundError(msg)

        logger.info(
            "Sending task to task manager for rotate image with id: %s and angle: %d",
            data.image_id,
            data.angle
        )

        await self._task_manager.rotate(image_id=typed_image_id, angle=data.angle)

        logger.info(
            "Successfully sent task to task manager for rotate image with id: %s and angle: %d",
            data.image_id,
            data.angle
        )
