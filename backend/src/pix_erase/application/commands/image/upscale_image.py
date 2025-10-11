import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from typing import final, Final, cast, Literal, Any, Coroutine
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.scheduler.payloads.images import UpscaleImagePayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskKey
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
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
            task_scheduler: TaskScheduler,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._scheduler: Final[TaskScheduler] = task_scheduler
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: UpscaleImageCommand) -> TaskID:
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

        task_id: TaskID = self._scheduler.make_task_id(
            key=TaskKey("upscale_image"),
            value=typed_image_id,
        )

        background_tasks: set[Task] = set()

        coroutine: Coroutine[Any, Any, None] = self._scheduler.schedule(
            task_id=task_id,
            payload=UpscaleImagePayload(
                image_id=typed_image_id,
                algorithm=data.algorithm,
                scale=ImageScale(data.scale),
            )
        )

        task: Task = asyncio.create_task(coroutine)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        logger.info(
            "Successfully send image for upscaling in task manager, image_id: %s, task_id: %s",
            image.id,
            task_id
        )

        return task_id
