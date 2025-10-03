import logging
from dataclasses import dataclass
from typing import final, Final, cast
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.image.task_manager import ImageTaskManager
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressImageCommand:
    image_id: UUID


@final
class CompressImageCommandHandler:
    def __init__(
            self,
            image_storage: ImageStorage,
            task_manager: ImageTaskManager,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._task_manager: Final[ImageTaskManager] = task_manager
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: CompressImageCommand) -> None:
        logger.info(
            "Started compressing image with id: %s",
            data.image_id,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        typed_image_id: ImageID = cast(ImageID, data.image_id)

        image: Image | None = await self._image_storage.read_by_id(image_id=typed_image_id)

        if image is None:
            msg = f"Failed to found image with id: {data.image_id}"
            raise ImageNotFoundError(msg)

        await self._task_manager.compress(image_id=typed_image_id)

        logger.info(
            "Successfully send image for compressing in task manager, image_id: %s",
            image.id,
        )
