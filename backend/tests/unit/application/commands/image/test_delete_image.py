from __future__ import annotations

from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from pix_erase.application.commands.image.delete_image import (
    DeleteImageCommand,
    DeleteImageCommandHandler,
)
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize


@pytest.mark.asyncio
async def test_delete_image_success(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_user_command_gateway: Mock,
    fake_transaction: Mock,
) -> None:
    # Arrange
    image_uuid = uuid4()
    image_id = ImageID(image_uuid)
    # current user has image
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]

    fake_image = Image(
        id=image_id,
        name=ImageName("x.jpg"),
        data=b"d",
        width=ImageSize(1),
        height=ImageSize(1),
    )
    fake_image_storage.read_by_id = AsyncMock(return_value=fake_image)  # type: ignore[attr-defined]
    fake_image_storage.delete_by_id = AsyncMock()  # type: ignore[attr-defined]
    fake_user_command_gateway.update = AsyncMock()  # type: ignore[attr-defined]

    sut = DeleteImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        user_command_gateway=fake_user_command_gateway,
        transaction_manager=fake_transaction,
    )

    # Act
    await sut(DeleteImageCommand(image_id=image_uuid))

    # Assert
    fake_image_storage.delete_by_id.assert_awaited()  # type: ignore[attr-defined]
    fake_user_command_gateway.update.assert_awaited()  # type: ignore[attr-defined]
    fake_transaction.commit.assert_awaited()  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_delete_image_not_found(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_user_command_gateway: Mock,
    fake_transaction: Mock,
) -> None:
    # Arrange
    image_uuid = uuid4()
    image_id = ImageID(image_uuid)
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]
    fake_image_storage.read_by_id = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = DeleteImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        user_command_gateway=fake_user_command_gateway,
        transaction_manager=fake_transaction,
    )

    # Act / Assert
    with pytest.raises(ImageNotFoundError):
        await sut(DeleteImageCommand(image_id=image_uuid))


@pytest.mark.asyncio
async def test_delete_image_wrong_owner(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_user_command_gateway: Mock,
    fake_transaction: Mock,
) -> None:
    # Arrange
    image_uuid = uuid4()
    image_id = ImageID(image_uuid)
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = []  # does not own

    fake_image = Image(
        id=image_id,
        name=ImageName("x.jpg"),
        data=b"d",
        width=ImageSize(1),
        height=ImageSize(1),
    )
    fake_image_storage.read_by_id = AsyncMock(return_value=fake_image)  # type: ignore[attr-defined]

    sut = DeleteImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        user_command_gateway=fake_user_command_gateway,
        transaction_manager=fake_transaction,
    )

    # Act / Assert
    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(DeleteImageCommand(image_id=image_uuid))
