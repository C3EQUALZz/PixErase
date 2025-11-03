import logging
import uuid
from typing import Annotated, Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import Context, TaskiqDepends, AsyncBroker
from taskiq.depends.progress_tracker import ProgressTracker, TaskState

from pix_erase.application.common.ports.image.comparison_gateway import ImageComparisonGateway
from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.entities.image_comparison import ImageComparison
from pix_erase.domain.image.services.colorization_service import ImageColorizationService
from pix_erase.domain.image.services.image_service import ImageService
from pix_erase.domain.image.services.transformation_service import ImageTransformationService
from pix_erase.domain.image.values.comparison_id import ComparisonID
from pix_erase.infrastructure.scheduler.tasks.schemas import (
    GrayscaleImageSchemaRequestTask,
    RotateImageSchemaRequestTask,
    CompressImageSchemaRequestTask,
    UpscaleImageSchemaRequestTask,
    RemoveBackgroundImageSchemaRequestTask,
    CompareImagesSchemaRequestTask,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


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

    colorization_service.convert_color_to_gray(image=image)  # type: ignore[arg-type]
    await file_storage.update(image=image)  # type: ignore[arg-type]

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    await progress_tracker.set_progress(state=TaskState.SUCCESS)


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
        image=image,  # type: ignore[arg-type]
        angle=request_schema.angle,
    )

    await file_storage.update(image=image)  # type: ignore[arg-type]

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Converted image to grayscale with id {request_schema.image_id}"
    )
    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
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
        image=image,  # type: ignore[arg-type]
        quality=request_schema.quality,
    )

    await file_storage.update(image=image)  # type: ignore[arg-type]

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Compressed image with id {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
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
        image=image,  # type: ignore[arg-type]
        algorithm=request_schema.algorithm,
        scale=request_schema.scale,
    )

    await file_storage.update(image=image)  # type: ignore[arg-type]

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Successfully upscaled image with id: {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
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

    colorization_service.remove_background(image=image)  # type: ignore[arg-type]
    await file_storage.update(image=image)  # type: ignore[arg-type]

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Successfully removed background image with id: {request_schema.image_id}"
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )


@inject(patch_module=True)
async def compare_images_task(
        request_schema: CompareImagesSchemaRequestTask,
        image_service: FromDishka[ImageService],
        file_storage: FromDishka[ImageStorage],
        comparison_gateway: FromDishka[ImageComparisonGateway],
        context: Annotated[Context, TaskiqDepends()],
        progress_tracker: Annotated[ProgressTracker, TaskiqDepends()],
) -> None:
    await progress_tracker.set_progress(
        state=TaskState.STARTED,
        meta=f"Started comparing images {request_schema.first_image_id} and {request_schema.second_image_id}",
    )

    logger.info(
        "Running task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )

    first_image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.first_image_id,
    )

    if first_image is None:
        msg = f"Image with id: {request_schema.first_image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg,
        )

        context.reject()
        return

    second_image: Image | None = await file_storage.read_by_id(
        image_id=request_schema.second_image_id,
    )

    if second_image is None:
        msg = f"Image with id: {request_schema.second_image_id} not found"
        logger.error(msg)

        await progress_tracker.set_progress(
            state=TaskState.FAILURE,
            meta=msg,
        )

        context.reject()
        return

    comparison_result = image_service.compare_images(
        first_image=first_image,
        second_image=second_image,
    )

    # Create comparison ID from concatenated image IDs (deterministic)
    # Sort IDs to ensure consistent comparison ID regardless of order
    sorted_ids = sorted([str(request_schema.first_image_id), str(request_schema.second_image_id)])
    comparison_id_str = f"{sorted_ids[0]}_{sorted_ids[1]}"
    comparison_id = ComparisonID(uuid.uuid5(uuid.NAMESPACE_DNS, comparison_id_str))

    comparison = ImageComparison(
        id=comparison_id,
        first_image_id=request_schema.first_image_id,
        second_image_id=request_schema.second_image_id,
        scores=comparison_result.scores,
        different_names=comparison_result.different_names,
        different_width=comparison_result.different_width,
        different_height=comparison_result.different_height,
    )

    await comparison_gateway.add(comparison)

    await progress_tracker.set_progress(
        state=TaskState.SUCCESS,
        meta=f"Successfully compared images {request_schema.first_image_id} and {request_schema.second_image_id}",
    )

    logger.info(
        "Finished task: %s with id: %s",
        context.message.task_name,
        context.message.task_id,
    )


def setup_images_task(broker: AsyncBroker) -> None:
    logger.info("Setup tasks")

    broker.register_task(
        func=convert_to_grayscale_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="grayscale_image"
    )

    broker.register_task(
        func=rotate_image_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="rotate_image"
    )

    broker.register_task(
        func=compress_image_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="compress_image"
    )

    broker.register_task(
        func=upscale_image_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="upscale_image"
    )

    broker.register_task(
        func=remove_background_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="remove_background_image"
    )

    broker.register_task(
        func=compare_images_task,
        retry_on_error=True,
        max_retries=3,
        delay=15,
        task_name="compare_images"
    )
