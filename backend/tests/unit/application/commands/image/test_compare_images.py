from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from pix_erase.application.commands.image.compare_images import (
    CompareImageCommand,
    CompareImageCommandHandler,
)
from pix_erase.application.common.ports.scheduler.task_id import TaskID
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize


@pytest.mark.asyncio
async def test_compare_images_schedules_task(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    # Arrange
    first_id = ImageID(uuid4())
    second_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [first_id, second_id]

    fake_first = Image(id=first_id, name=ImageName("a.jpg"), data=b"d", width=ImageSize(1), height=ImageSize(1))
    fake_second = Image(id=second_id, name=ImageName("b.jpg"), data=b"d", width=ImageSize(1), height=ImageSize(1))
    fake_image_storage.read_by_id = AsyncMock(side_effect=[fake_first, fake_second])  # type: ignore[attr-defined]
    expected: TaskID = TaskID("compare_images:1")
    fake_task_scheduler.make_task_id.return_value = expected  # type: ignore[assignment]
    fake_task_scheduler.schedule = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = CompareImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
    )

    # Act
    result = await sut(CompareImageCommand(first_image=first_id, second_image=second_id))

    # Assert
    assert result == expected
    fake_task_scheduler.schedule.assert_called_once()  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_compare_images_wrong_owner_first(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    first_id = ImageID(uuid4())
    second_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [second_id]

    sut = CompareImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
    )
    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(CompareImageCommand(first_image=first_id, second_image=second_id))


@pytest.mark.asyncio
async def test_compare_images_wrong_owner_second(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    first_id = ImageID(uuid4())
    second_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [first_id]

    sut = CompareImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
    )
    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(CompareImageCommand(first_image=first_id, second_image=second_id))


@pytest.mark.asyncio
async def test_compare_images_first_not_found(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    first_id = ImageID(uuid4())
    second_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [first_id, second_id]
    fake_image_storage.read_by_id = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = CompareImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
    )
    with pytest.raises(ImageNotFoundError):
        await sut(CompareImageCommand(first_image=first_id, second_image=second_id))


@pytest.mark.asyncio
async def test_compare_images_second_not_found(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    first_id = ImageID(uuid4())
    second_id = ImageID(uuid4())
    user = await fake_current_user_service.get_current_user()
    user.images = [first_id, second_id]
    fake_first = Image(id=first_id, name=ImageName("a.jpg"), data=b"d", width=ImageSize(1), height=ImageSize(1))
    fake_image_storage.read_by_id = AsyncMock(side_effect=[fake_first, None])  # type: ignore[attr-defined]

    sut = CompareImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        scheduler=fake_task_scheduler,
    )
    with pytest.raises(ImageNotFoundError):
        await sut(CompareImageCommand(first_image=first_id, second_image=second_id))
