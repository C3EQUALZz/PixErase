import logging
from dataclasses import dataclass
from typing import final, Final, cast, Literal
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.image.task_manager import ImageTaskManager
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_scale import ImageScale
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class UpscaleImageCommand:
    image_id: UUID
    algorithm: Literal["AI", "NearestNeighbour"]
    scale: int


@final
class UpscaleImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing photo that user uploaded before.
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

    async def __call__(self, data: UpscaleImageCommand) -> None:
        logger.info(
            "Started upscaling image with id: %s",
            data.image_id,
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

        logger.info("Sending task for upscaling image with id: %s", data.image_id)

        await self._task_manager.upscale(
            image_id=typed_image_id,
            algorithm=data.algorithm,
            scale=ImageScale(data.scale),
        )

        logger.info("Successfully send task for upscaling image with id: %s", data.image_id)
