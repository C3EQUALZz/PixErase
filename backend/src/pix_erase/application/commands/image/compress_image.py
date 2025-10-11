import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from typing import final, Final, cast, Coroutine, Any
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.scheduler.payloads.images import CompressImagePayload
from pix_erase.application.common.ports.scheduler.task_id import TaskKey, TaskID
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageNotFoundError, ImageDoesntBelongToThisUserError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressImageCommand:
    image_id: UUID
    quality: int


@final
class CompressImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Changes existing image.
    """

    def __init__(
            self,
            image_storage: ImageStorage,
            scheduler: TaskScheduler,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._task_scheduler: Final[TaskScheduler] = scheduler
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: CompressImageCommand) -> TaskID:
        logger.info(
            "Started compressing image with id: %s",
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

        task_id: TaskID = self._task_scheduler.make_task_id(
            key=TaskKey("compress_image"),
            value=typed_image_id,
        )

        background_tasks: set[Task] = set()

        coroutine: Coroutine[Any, Any, None] = self._task_scheduler.schedule(
            task_id=task_id,
            payload=CompressImagePayload(
                image_id=typed_image_id,
                quality=data.quality,
            ),
        )

        task: Task = asyncio.create_task(coroutine)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        logger.info(
            "Successfully send image for compressing in task manager, image_id: %s, task_id: %s",
            image.id,
            task_id
        )

        return task_id
