from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from pix_erase.application.common.ports.image.extractor import (
    CameraSettings,
    DateTimeInfo,
    ExposureSettings,
    FlashInfo,
    FlashMode,
    GPSInfo,
    ImageInfo,
    ImageInfoExtractor,
    MeteringMode,
    Orientation,
    WhiteBalance,
)
from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.query_models.image import ImageStreamQueryModel
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.application.queries.images.read_exif_from_image_by_id import (
    ReadExifFromImageByIDQuery,
    ReadExifFromImageByIDQueryHandler,
)
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize
from pix_erase.domain.user.values.user_role import UserRole


async def _single_chunk_stream() -> AsyncGenerator[bytes, None]:
    yield b"payload"


@pytest.mark.asyncio
async def test_read_exif_success(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
    fake_image_extractor: ImageInfoExtractor,
) -> None:
    # Arrange
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]

    stream_model = ImageStreamQueryModel(
        stream=_single_chunk_stream(),
        content_type="image/jpeg",
        content_length=7,
        width=ImageSize(100),
        height=ImageSize(50),
        filename=ImageName("exif.jpg"),
        etag=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    fake_image_storage.stream_by_id = AsyncMock(return_value=stream_model)  # type: ignore[attr-defined]

    image_info = ImageInfo(
        width=100,
        height=50,
        format="JPEG",
        is_animated=False,
        camera=CameraSettings(make="Canon", model="X", orientation=Orientation.TOP_LEFT, focal_length="50mm"),
        exposure=ExposureSettings(
            exposure_time="1/100",
            aperture="f/1.8",
            iso=200,
            exposure_bias="0",
            metering_mode=MeteringMode.AVERAGE,
            white_balance=WhiteBalance.AUTO,
        ),
        flash=FlashInfo(
            fired=True, mode=FlashMode.FIRED, return_light=False, function_present=True, red_eye_reduction=False
        ),
        gps=GPSInfo(latitude=1.0, longitude=2.0, altitude=3.0, latitude_ref="N", longitude_ref="E"),
        datetime_info=DateTimeInfo(created=datetime.now(UTC), digitized=datetime.now(UTC), original=datetime.now(UTC)),
    )

    fake_image_extractor.extract = AsyncMock(return_value=image_info)  # type: ignore[attr-defined]

    sut = ReadExifFromImageByIDQueryHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        image_extractor=fake_image_extractor,
    )

    # Act
    view = await sut(ReadExifFromImageByIDQuery(image_id=image_id))

    # Assert
    assert view.width == 100
    assert view.height == 50
    assert view.format == "JPEG"
    assert view.camera_settings.make == "Canon"
    assert view.exposure_settings.iso == 200
    assert view.flash_info.fired is True
    assert view.gps_info.latitude == 1.0


@pytest.mark.asyncio
async def test_read_exif_forbidden_when_not_owner(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
    fake_image_extractor: ImageInfoExtractor,
) -> None:
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = []
    current_user.role = UserRole.USER

    sut = ReadExifFromImageByIDQueryHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        image_extractor=fake_image_extractor,
    )

    with pytest.raises(ImageDoesntBelongToThisUserError):
        await sut(ReadExifFromImageByIDQuery(image_id=image_id))


@pytest.mark.asyncio
async def test_read_exif_not_found(
    fake_current_user_service: CurrentUserService,
    fake_image_storage: ImageStorage,
    fake_image_extractor: ImageInfoExtractor,
) -> None:
    image_id = ImageID(uuid4())
    current_user = await fake_current_user_service.get_current_user()
    current_user.images = [image_id]

    fake_image_storage.stream_by_id = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = ReadExifFromImageByIDQueryHandler(
        current_user_service=fake_current_user_service,
        image_storage=fake_image_storage,
        image_extractor=fake_image_extractor,
    )

    with pytest.raises(ImageNotFoundError):
        await sut(ReadExifFromImageByIDQuery(image_id=image_id))
