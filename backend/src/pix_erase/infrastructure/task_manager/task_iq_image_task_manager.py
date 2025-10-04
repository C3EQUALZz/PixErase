import logging
from typing import Final
from typing import cast

from taskiq import AsyncTaskiqTask
from typing_extensions import override

from pix_erase.application.common.ports.image.task_manager import ImageTaskManager, TaskID
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.infrastructure.task_manager.images_tasks import (
    convert_to_grayscale_task,
    rotate_image_task,
    compress_image_task
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class TaskIQImageTaskManager(ImageTaskManager):
    def __init__(self, image_id_generator: ImageIdGenerator) -> None:
        self._image_id_generator: Final[ImageIdGenerator] = image_id_generator

    @override
    async def convert_to_grayscale(self, image_id: ImageID) -> TaskID:
        task: AsyncTaskiqTask = await convert_to_grayscale_task.kiq(image_id=image_id)
        return cast(TaskID, task.task_id)

    @override
    async def compress(self, image_id: ImageID, quality: int) -> TaskID:
        task: AsyncTaskiqTask = await compress_image_task.kiq(image_id=image_id, quality=quality)
        return cast(TaskID, task.task_id)

    @override
    async def rotate(self, image_id: ImageID, angle: int) -> TaskID:
        task: AsyncTaskiqTask = await rotate_image_task.kiq(image_id=image_id, angle=angle)
        return cast(TaskID, task.task_id)
