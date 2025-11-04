import logging
from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final, cast, final
from uuid import UUID

from pix_erase.application.common.ports.image.extractor import ImageInfo, ImageInfoExtractor
from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.image.read_image import (
    CameraOrientationView,
    CameraSettingsExifView,
    DateTimeInfoView,
    ExposureSettingsView,
    FlashInfoView,
    FlashModeView,
    GPSInfoView,
    MeteringModeView,
    ReadImageExifView,
    WhiteBalanceView,
)
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.application.common.query_models.image import ImageStreamQueryModel
    from pix_erase.domain.image.values.image_id import ImageID
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)
UNKNOWN_FIELD: Final[str] = "unknown"


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadExifFromImageByIDQuery:
    image_id: UUID


@final
class ReadExifFromImageByIDQueryHandler:
    """
    - Only current user can read exif from his images.
    - Admins and super admins can read exif from every image.
    - Opens to everyone.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        image_storage: ImageStorage,
        image_extractor: ImageInfoExtractor,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._image_storage: Final[ImageStorage] = image_storage
        self._image_extractor: Final[ImageInfoExtractor] = image_extractor

    async def __call__(self, data: ReadExifFromImageByIDQuery) -> ReadImageExifView:
        logger.info(
            "Started reading exif from image by id: %s",
            data.image_id,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        typed_image_id: ImageID = cast("ImageID", data.image_id)

        if (
            current_user.role not in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
            and typed_image_id not in current_user.images
        ):
            msg = f"Image with id: {data.image_id}, doesn't belong to user with id: {current_user.id}"
            raise ImageDoesntBelongToThisUserError(msg)

        stream: ImageStreamQueryModel | None = await self._image_storage.stream_by_id(typed_image_id)

        if stream is None:
            msg = f"Image with id {data.image_id} not found"
            raise ImageNotFoundError(msg)

        logger.debug("Started collecting chunks from image storage, image id: %s", data.image_id)
        collected_chunks: deque[bytes] = deque()

        async for chunk in stream.stream:
            collected_chunks.append(chunk)

        image_info_dto: ImageInfo = await self._image_extractor.extract(data=b"".join(collected_chunks))
        logger.debug("Successfully got image info by id: %s", data.image_id)

        image_format: str = image_info_dto.format if image_info_dto.format is not None else UNKNOWN_FIELD
        camera_settings: CameraSettingsExifView
        exposure_settings: ExposureSettingsView

        if image_info_dto.camera is None:
            logger.debug("Image info about camera is None, image id: %s, setting default fields", data.image_id)

            camera_settings = CameraSettingsExifView(
                make=UNKNOWN_FIELD,
                model=UNKNOWN_FIELD,
                orientation=CameraOrientationView.UNKNOWN,
                focal_length=UNKNOWN_FIELD,
                focal_length_35mm=UNKNOWN_FIELD,
                max_aperture=UNKNOWN_FIELD,
                aperture_value=UNKNOWN_FIELD,
            )

            logger.debug("Successfully set default camera settings: camera_settings: %s", camera_settings)

        else:
            make: str

            make = image_info_dto.camera.make if image_info_dto.camera.make is not None else UNKNOWN_FIELD

            model: str

            model = image_info_dto.camera.model if image_info_dto.camera.model is not None else UNKNOWN_FIELD

            orientation: CameraOrientationView

            if image_info_dto.camera.orientation is not None:
                orientation = CameraOrientationView[image_info_dto.camera.orientation.name]
            else:
                orientation = CameraOrientationView.UNKNOWN

            focal_length: str

            focal_length = image_info_dto.camera.focal_length or UNKNOWN_FIELD

            focal_length_35mm: str

            if image_info_dto.camera.focal_length_35mm is not None:
                focal_length_35mm = image_info_dto.camera.focal_length_35mm
            else:
                focal_length_35mm = UNKNOWN_FIELD

            max_aperture: str

            if image_info_dto.camera.max_aperture is not None:
                max_aperture = image_info_dto.camera.max_aperture
            else:
                max_aperture = UNKNOWN_FIELD

            aperture_value: str

            aperture_value = image_info_dto.camera.aperture_value or UNKNOWN_FIELD

            camera_settings = CameraSettingsExifView(
                make=make,
                model=model,
                orientation=orientation,
                focal_length=focal_length,
                focal_length_35mm=focal_length_35mm,
                max_aperture=max_aperture,
                aperture_value=aperture_value,
            )

        if image_info_dto.exposure is None:
            exposure_settings = ExposureSettingsView(
                exposure_time=UNKNOWN_FIELD,
                aperture=UNKNOWN_FIELD,
                iso=100,
                exposure_bias=UNKNOWN_FIELD,
                metering_mode=MeteringModeView.UNKNOWN,
                white_balance=WhiteBalanceView.UNKNOWN,
            )
        else:
            exposure_time: str

            if image_info_dto.exposure.exposure_time is not None:
                exposure_time = image_info_dto.exposure.exposure_time
            else:
                exposure_time = UNKNOWN_FIELD

            aperture: str

            if image_info_dto.exposure.aperture is not None:
                aperture = image_info_dto.exposure.aperture
            else:
                aperture = UNKNOWN_FIELD

            iso: int

            iso = image_info_dto.exposure.iso if image_info_dto.exposure.iso is not None else 100

            exposure_bias: str

            exposure_bias = image_info_dto.exposure.exposure_bias or UNKNOWN_FIELD

            metering_mode: MeteringModeView

            if image_info_dto.exposure.metering_mode is not None:
                metering_mode = MeteringModeView[image_info_dto.exposure.metering_mode.name]
            else:
                metering_mode = MeteringModeView.UNKNOWN

            white_balance: WhiteBalanceView

            if image_info_dto.exposure.white_balance is not None:
                white_balance = WhiteBalanceView[image_info_dto.exposure.white_balance.name]
            else:
                white_balance = WhiteBalanceView.UNKNOWN

            exposure_settings = ExposureSettingsView(
                exposure_time=exposure_time,
                aperture=aperture,
                iso=iso,
                exposure_bias=exposure_bias,
                metering_mode=metering_mode,
                white_balance=white_balance,
            )

        flash_info_view: FlashInfoView

        if image_info_dto.flash is None:
            flash_info_view = FlashInfoView(
                fired=False,
                mode=FlashModeView.UNKNOWN,
                return_light=False,
                function_present=False,
                red_eye_reduction=False,
            )
        else:
            mode: FlashModeView

            mode = FlashModeView[image_info_dto.flash.mode.name] if image_info_dto.flash.mode else FlashModeView.UNKNOWN

            flash_info_view = FlashInfoView(
                fired=image_info_dto.flash.fired,
                mode=mode,
                return_light=image_info_dto.flash.return_light,
                function_present=image_info_dto.flash.function_present,
                red_eye_reduction=image_info_dto.flash.red_eye_reduction,
            )

        gps_info: GPSInfoView

        if image_info_dto.gps is None:
            gps_info = GPSInfoView(
                latitude=0.0,
                longitude=0.0,
                altitude=0.0,
                latitude_ref=UNKNOWN_FIELD,
                longitude_ref=UNKNOWN_FIELD,
            )
        else:
            latitude: float

            latitude = image_info_dto.gps.latitude if image_info_dto.gps.latitude is not None else 0.0

            longitude: float

            longitude = image_info_dto.gps.longitude if image_info_dto.gps.longitude is not None else 0.0

            altitude: float

            altitude = image_info_dto.gps.altitude if image_info_dto.gps.altitude is not None else 0.0

            latitude_ref: str

            if image_info_dto.gps.latitude_ref is not None:
                latitude_ref = image_info_dto.gps.latitude_ref
            else:
                latitude_ref = UNKNOWN_FIELD

            longitude_ref: str

            if image_info_dto.gps.longitude_ref is not None:
                longitude_ref = image_info_dto.gps.longitude_ref
            else:
                longitude_ref = UNKNOWN_FIELD

            gps_info = GPSInfoView(
                latitude=latitude,
                longitude=longitude,
                altitude=altitude,
                latitude_ref=latitude_ref,
                longitude_ref=longitude_ref,
            )

        datetime_info: DateTimeInfoView

        if image_info_dto.datetime_info is None:
            datetime_info = DateTimeInfoView(
                created=datetime.now(UTC),
                digitized=datetime.now(UTC),
                original=datetime.now(UTC),
            )
        else:
            created: datetime

            if image_info_dto.datetime_info.created is not None:
                created = image_info_dto.datetime_info.created
            else:
                created = datetime.now(UTC)

            digitized: datetime

            if image_info_dto.datetime_info.digitized is not None:
                digitized = image_info_dto.datetime_info.digitized
            else:
                digitized = datetime.now(UTC)

            original: datetime

            if image_info_dto.datetime_info.original is not None:
                original = image_info_dto.datetime_info.original
            else:
                original = datetime.now(UTC)

            datetime_info = DateTimeInfoView(
                created=created,
                digitized=digitized,
                original=original,
            )

        return ReadImageExifView(
            width=image_info_dto.width,
            height=image_info_dto.height,
            format=image_format,
            is_animated=image_info_dto.is_animated,
            camera_settings=camera_settings,
            exposure_settings=exposure_settings,
            flash_info=flash_info_view,
            gps_info=gps_info,
            datetime_info=datetime_info,
        )
