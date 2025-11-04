from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from pix_erase.application.commands.image.grayscale_image import (
    ConvertImageToGrayscaleCommand,
    GrayscaleImageCommandHandler,
)
from pix_erase.application.common.ports.scheduler.task_id import TaskID
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize


@pytest.mark.asyncio
async def test_grayscale_image_schedules_task(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    # Arrange
    image_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [image_id]

    fake_image = Image(id=image_id, name=ImageName("a.jpg"), data=b"d", width=ImageSize(1), height=ImageSize(1))
    fake_image_storage.read_by_id = AsyncMock(return_value=fake_image)  # type: ignore[attr-defined]
    expected: TaskID = TaskID("grayscale_image:1")
    fake_task_scheduler.make_task_id.return_value = expected  # type: ignore[assignment]
    fake_task_scheduler.schedule = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = GrayscaleImageCommandHandler(
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
        current_user_service=fake_current_user_service,
    )

    # Act
    result = await sut(ConvertImageToGrayscaleCommand(image_id=image_id))

    # Assert
    assert result == expected
    fake_task_scheduler.schedule.assert_called_once()  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_grayscale_image_wrong_owner(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    image_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = []

    sut = GrayscaleImageCommandHandler(
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
        current_user_service=fake_current_user_service,
    )
    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(ConvertImageToGrayscaleCommand(image_id=image_id))


@pytest.mark.asyncio
async def test_grayscale_image_not_found(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    image_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [image_id]
    fake_image_storage.read_by_id = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = GrayscaleImageCommandHandler(
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
        current_user_service=fake_current_user_service,
    )
    with pytest.raises(ImageNotFoundError):
        await sut(ConvertImageToGrayscaleCommand(image_id=image_id))
