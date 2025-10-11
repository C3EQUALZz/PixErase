import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from datetime import timedelta, datetime, UTC
from typing import final, Final, cast, Coroutine, Any
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.scheduler.payloads.images import RemoveImageBackgroundPayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskKey
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RemoveBackgroundImageCommand:
    image_id: UUID


@final
class RemoveBackgroundImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Changes existing image.
    """

    def __init__(
            self,
            scheduler: TaskScheduler,
            image_storage: ImageStorage,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._scheduler: Final[TaskScheduler] = scheduler
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: RemoveBackgroundImageCommand) -> TaskID:
        logger.info(
            "Started converting image to grayscale, image_name: %s",
            data.image_id
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

        task_id: TaskID = self._scheduler.make_task_id(
            key=TaskKey("remove_background_image"),
            value=typed_image_id,
        )

        background_tasks: set[Task] = set()

        coroutine: Coroutine[Any, Any, None] = self._scheduler.schedule_by_time(
            task_id=task_id,
            payload=RemoveImageBackgroundPayload(
                image_id=typed_image_id,
            ),
            run_at=datetime.now(UTC) + timedelta(seconds=5)
        )

        task: Task = asyncio.create_task(coroutine)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        logger.info(
            "Successfully send image for grayscaling in task manager, image_id: %s, task_id: %s",
            image.id,
            task_id
        )

        return task_id
