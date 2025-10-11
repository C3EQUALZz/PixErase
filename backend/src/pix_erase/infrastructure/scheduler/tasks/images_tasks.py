import logging
from typing import Annotated, Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import Context, TaskiqDepends
from taskiq.brokers.shared_broker import shared_task
from taskiq.depends.progress_tracker import ProgressTracker, TaskState

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.services.colorization_service import ImageColorizationService
from pix_erase.domain.image.services.transformation_service import ImageTransformationService
from pix_erase.domain.image.values.image_scale import ImageScale
from pix_erase.infrastructure.scheduler.tasks.schemas import (
    GrayscaleImageSchemaRequestTask,
    RotateImageSchemaRequestTask,
    CompressImageSchemaRequestTask,
    UpscaleImageSchemaRequestTask,
    RemoveBackgroundImageSchemaRequestTask
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15,
    task_name="grayscale_image"
)
@inject(patch_module=True)
async def convert_to_grayscale_task(
        request_schema: GrayscaleImageSchemaRequestTask,
        colorization_service: FromDishka[ImageColorizationService],
        file_storage: FromDishka[ImageStorage],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()]
) -> None:
    await progress_tracker.set_progress(
        state=TaskState.STARTED,
        meta=f"Started converting image to grayscale with id {request_schema.image_id}"
    )

    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.image_id
    )

    if image is None:
        msg = f"image with id: {request_schema.image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg
        )

        context.reject()

    colorization_service.convert_color_to_gray(image=image)
    await file_storage.update(image=image)

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    await progress_tracker.set_progress(state=TaskState.SUCCESS)


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15,
    task_name="rotate_image"
)
@inject(patch_module=True)
async def rotate_image_task(
        request_schema: RotateImageSchemaRequestTask,
        file_storage: FromDishka[ImageStorage],
        image_transformation_service: FromDishka[ImageTransformationService],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()]
) -> None:
    await progress_tracker.set_progress(
        state=TaskState.STARTED,
        meta=f"Started converting image to grayscale with id {request_schema.image_id}"
    )

    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.image_id
    )

    if image is None:
        msg = f"image with id: {request_schema.image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg
        )

        context.reject()

    image_transformation_service.rotate_image(
        image=image,
        angle=request_schema.angle,
    )

    await file_storage.update(image=image)

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Converted image to grayscale with id {request_schema.image_id}"
    )
    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15,
    task_name="compress_image"
)
@inject(patch_module=True)
async def compress_image_task(
        request_schema: CompressImageSchemaRequestTask,
        image_transformation_service: FromDishka[ImageTransformationService],
        file_storage: FromDishka[ImageStorage],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()]
) -> None:
    await progress_tracker.set_progress(
        state=TaskState.STARTED,
        meta=f"Started compressing image to grayscale with id {request_schema.image_id}"
    )

    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.image_id
    )

    if image is None:
        msg = f"image with id: {request_schema.image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg
        )

        context.reject()

    image_transformation_service.compress_image(
        image=image,
        quality=request_schema.quality,
    )

    await file_storage.update(image=image)

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Compressed image with id {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15,
    task_name="upscale_image"
)
@inject(patch_module=True)
async def upscale_image_task(
        request_schema: UpscaleImageSchemaRequestTask,
        image_colorization_service: FromDishka[ImageColorizationService],
        file_storage: FromDishka[ImageStorage],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()]
) -> None:
    await progress_tracker.set_progress(
        state=TaskState.STARTED,
        meta=f"Started upscaling image with id: {request_schema.image_id}"
    )

    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.image_id
    )

    if image is None:
        msg = f"image with id: {request_schema.image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg
        )

        context.reject()

    image_colorization_service.upscale(
        image=image,
        algorithm=request_schema.algorithm,
        scale=ImageScale(request_schema.scale),
    )

    await file_storage.update(image=image)

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Successfully upscaled image with id: {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )


@shared_task(
    retry_on_error=True,
    max_retries=3,
    delay=15,
    task_name="remove_background_image"
)
@inject(patch_module=True)
async def remove_background_task(
        request_schema: RemoveBackgroundImageSchemaRequestTask,
        colorization_service: FromDishka[ImageColorizationService],
        file_storage: FromDishka[ImageStorage],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()]
) -> None:
    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.image_id
    )

    if image is None:
        msg = f"image with id: {request_schema.image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg
        )

        context.reject()

    colorization_service.remove_background(image=image)
    await file_storage.update(image=image)

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Successfully removed background image with id: {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )
