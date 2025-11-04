import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final, cast, final
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.scheduler.payloads.images import CompareImagesPayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskKey
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError

if TYPE_CHECKING:
    from collections.abc import Coroutine

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
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Returns TaskID for tracking comparison progress.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        image_storage: ImageStorage,
        scheduler: TaskScheduler,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._image_storage: Final[ImageStorage] = image_storage
        self._task_scheduler: Final[TaskScheduler] = scheduler

    async def __call__(self, data: CompareImageCommand) -> TaskID:
        logger.info(
            "Started comparing images. First image id: %s, second image id: %s",
            data.first_image,
            data.second_image,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        typed_first_image_id: ImageID = cast("ImageID", data.first_image)
        typed_second_image_id: ImageID = cast("ImageID", data.second_image)

        if typed_first_image_id not in current_user.images:
            msg = f"Image with id: {data.first_image} doesn't belong to this user."
            raise ImageDoesntBelongToThisUserError(msg)

        if typed_second_image_id not in current_user.images:
            msg = f"Image with id: {data.second_image} doesn't belong to this user."
            raise ImageDoesntBelongToThisUserError(msg)

        first_image: Image | None = await self._image_storage.read_by_id(image_id=typed_first_image_id)

        if first_image is None:
            msg = f"Failed to found image with id: {data.first_image}"
            raise ImageNotFoundError(msg)

        second_image: Image | None = await self._image_storage.read_by_id(image_id=typed_second_image_id)

        if second_image is None:
            msg = f"Failed to found image with id: {data.second_image}"
            raise ImageNotFoundError(msg)

        # Create task ID from concatenated image IDs
        task_id_value = f"{typed_first_image_id}_{typed_second_image_id}"
        task_id: TaskID = self._task_scheduler.make_task_id(
            key=TaskKey("compare_images"),
            value=task_id_value,
        )

        background_tasks: set[Task] = set()

        coroutine: Coroutine[Any, Any, None] = self._task_scheduler.schedule(
            task_id=task_id,
            payload=CompareImagesPayload(
                first_image_id=typed_first_image_id,
                second_image_id=typed_second_image_id,
            ),
        )

        task: Task = asyncio.create_task(coroutine)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        logger.info(
            "Successfully sent images for comparison in task manager, "
            "first_image_id: %s, second_image_id: %s, task_id: %s",
            typed_first_image_id,
            typed_second_image_id,
            task_id,
        )

        return task_id
