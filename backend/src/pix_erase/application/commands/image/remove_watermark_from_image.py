import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RemoveWatermarkFromImageCommand:
    image_id: UUID
    use_ai: bool


@final
class RemoveWatermarkFromImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Changes existing image.
    """

    def __init__(
            self,
            image_storage: ImageStorage,
            task_scheduler: TaskScheduler,
            current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._task_scheduler: Final[TaskScheduler] = task_scheduler
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: RemoveWatermarkFromImageCommand) -> None:
        logger.info(
            "Started removing watermark from image with id: %s, using ai: %s",
            data.image_id,
            data.use_ai,
        )


