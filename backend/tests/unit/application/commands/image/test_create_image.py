from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from pix_erase.application.commands.image.create_image import (
    CreateImageCommand,
    CreateImageCommandHandler,
)
from pix_erase.application.common.ports.image.extractor import ImageInfo
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize

if TYPE_CHECKING:
    from pix_erase.application.common.views.image.create_image import CreateImageView


@pytest.mark.asyncio
async def test_create_image_success(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_image_extractor: Mock,
    fake_image_service: Mock,
    fake_user_service: Mock,
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
) -> None:
    # Arrange
    data = b"image-bytes"
    filename = "test.jpg"
    fake_image_extractor.extract = AsyncMock(
        return_value=ImageInfo(  # type: ignore[attr-defined]
            height=100,
            width=200,
        )
    )
    new_id = ImageID(uuid4())
    new_image = Image(id=new_id, name=ImageName(filename), height=ImageSize(100), width=ImageSize(200), data=data)
    fake_image_service.create.return_value = new_image  # type: ignore[assignment]
    fake_image_storage.add = AsyncMock()  # type: ignore[attr-defined]
    fake_user_command_gateway.update = AsyncMock()  # type: ignore[attr-defined]

    sut = CreateImageCommandHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        image_extractor=fake_image_extractor,
        image_service=fake_image_service,
        user_service=fake_user_service,
        transaction_manager=fake_transaction,
        user_command_gateway=fake_user_command_gateway,
    )

    cmd = CreateImageCommand(data=data, filename=filename)

    # Act
    view: CreateImageView = await sut(cmd)

    # Assert
    assert view.image_id == new_id
    fake_image_extractor.extract.assert_awaited()  # type: ignore[attr-defined]
    fake_image_storage.add.assert_awaited()  # type: ignore[attr-defined]
    fake_user_command_gateway.update.assert_awaited()  # type: ignore[attr-defined]
    fake_transaction.flush.assert_awaited()  # type: ignore[attr-defined]
    fake_transaction.commit.assert_awaited()  # type: ignore[attr-defined]
