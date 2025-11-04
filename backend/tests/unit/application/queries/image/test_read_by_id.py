from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.query_models.image import ImageStreamQueryModel
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.application.queries.images.read_by_id import ReadImageByIDQuery, ReadImageByIDQueryHandler
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.application.common.views.image.read_image import ReadImageByIDView


async def _bytes_stream(chunks: list[bytes]) -> AsyncGenerator[bytes, None]:
    for c in chunks:
        yield c


@pytest.mark.asyncio
async def test_read_image_by_id_success(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
) -> None:
    # Arrange
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]

    chunks = [
        b"abc",
        b"def",
    ]

    stream_model = ImageStreamQueryModel(
        stream=_bytes_stream(chunks=chunks),
        content_type="image/jpeg",
        content_length=6,
        width=ImageSize(640),
        height=ImageSize(480),
        filename=ImageName("photo.jpg"),
        etag="etag123",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    fake_image_storage.stream_by_id = AsyncMock(return_value=stream_model)  # type: ignore[attr-defined]

    sut = ReadImageByIDQueryHandler(image_storage=fake_image_storage, current_user_service=fake_current_user_service)
    query = ReadImageByIDQuery(image_id=image_id)

    # Act
    view: ReadImageByIDView = await sut(query)

    # Assert
    assert view.name == str(stream_model.filename)
    assert view.width == stream_model.width.value
    assert view.height == stream_model.height.value
    assert view.content_type == stream_model.content_type
    assert view.content_length == stream_model.content_length
    assert view.etag == stream_model.etag

    # consume stream and verify content
    received: bytearray = bytearray()
    async for part in view.data:
        received.extend(part)
    assert bytes(received) == b"".join(chunks)


@pytest.mark.asyncio
async def test_read_image_by_id_forbidden_when_not_owner(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
) -> None:
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = []  # not owner and not admin
    current_user.role = UserRole.USER

    sut = ReadImageByIDQueryHandler(image_storage=fake_image_storage, current_user_service=fake_current_user_service)

    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(ReadImageByIDQuery(image_id=image_id))


@pytest.mark.asyncio
async def test_read_image_by_id_admin_bypass_ownership(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
) -> None:
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = []  # no ownership but admin
    current_user.role = UserRole.ADMIN

    # minimal stream
    stream_model = ImageStreamQueryModel(
        stream=_bytes_stream([b"x"]),
        content_type="image/png",
        content_length=1,
        width=ImageSize(1),
        height=ImageSize(1),
        filename=ImageName("x.png"),
        etag=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_image_storage.stream_by_id = AsyncMock(return_value=stream_model)  # type: ignore[attr-defined]

    sut = ReadImageByIDQueryHandler(image_storage=fake_image_storage, current_user_service=fake_current_user_service)
    view = await sut(ReadImageByIDQuery(image_id=image_id))
    assert view.name == "x.png"


@pytest.mark.asyncio
async def test_read_image_by_id_not_found(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
) -> None:
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]
    fake_image_storage.stream_by_id = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = ReadImageByIDQueryHandler(image_storage=fake_image_storage, current_user_service=fake_current_user_service)

    with pytest.raises(ImageNotFoundError):
        await sut(ReadImageByIDQuery(image_id=image_id))
