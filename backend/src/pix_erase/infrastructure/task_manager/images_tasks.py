import logging
from typing import Annotated, Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import Context, TaskiqDepends
from taskiq.brokers.shared_broker import shared_task

from pix_erase.application.common.services.colorization_service import ColorizationService
from pix_erase.domain.image.values.image_id import ImageID

logger: Final[logging.Logger] = logging.getLogger(__name__)


@shared_task(retry_on_error=True, max_retries=3, delay=15)
@inject(patch_module=True)
async def convert_to_grayscale_task(
        image_id: ImageID,
        colorization_service: FromDishka[ColorizationService],
        context: Annotated[Context, TaskiqDepends()]
) -> None:
    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    await colorization_service.convert_to_grayscale(image_id)

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )