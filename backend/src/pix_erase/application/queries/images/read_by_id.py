import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, cast, final
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.image.read_image import ReadImageByIDView
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.application.common.query_models.image import ImageStreamQueryModel
    from pix_erase.domain.image.values.image_id import ImageID
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadImageByIDQuery:
    image_id: UUID


@final
class ReadImageByIDQueryHandler:
    """
    - Opens to everyone
    - Admins and Super Admins can read images from all users
    - Usual user can read only his images
    - Returns stream for better performance
    """

    def __init__(
        self,
        image_storage: ImageStorage,
        current_user_service: CurrentUserService,
    ) -> None:
        self._image_storage: Final[ImageStorage] = image_storage
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ReadImageByIDQuery) -> ReadImageByIDView:
        logger.info("Started reading image by id, id of the image: %s", data.image_id)

        logger.info("Started getting current user for reading image by id: %s", data.image_id)
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user: %s, while reading image by id: %s", current_user.id, data.image_id)

        typed_image_id: ImageID = cast("ImageID", data.image_id)

        if (
            current_user.role not in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
            and typed_image_id not in current_user.images
        ):
            msg = f"Image with id: {data.image_id}, doesn't belong to user with id: {current_user.id}"
            raise ImageDoesntBelongToThisUserError(msg)

        logger.info("Started requesting stream for reading image by id: %s", data.image_id)

        stream: ImageStreamQueryModel | None = await self._image_storage.stream_by_id(typed_image_id)

        if stream is None:
            msg = f"Image with id {data.image_id} not found"
            raise ImageNotFoundError(msg)

        logger.info("Stream by image id: %s is not None, returning data to view", data.image_id)

        view: ReadImageByIDView = ReadImageByIDView(
            data=stream.stream,
            name=stream.filename.value,
            height=stream.height.value,
            width=stream.width.value,
            content_type=stream.content_type,
            content_length=stream.content_length,
            created_at=stream.created_at,
            updated_at=stream.updated_at,
            etag=stream.etag,
        )

        logger.info("Finished retrieving stream for reading image by id: %s", data.image_id)

        return view
