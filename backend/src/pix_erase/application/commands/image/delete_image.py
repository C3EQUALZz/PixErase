import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, cast, final
from uuid import UUID

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.image import ImageDoesntBelongToThisUserError, ImageNotFoundError

if TYPE_CHECKING:
    from pix_erase.domain.image.entities.image import Image
    from pix_erase.domain.image.values.image_id import ImageID
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteImageCommand:
    image_id: UUID


@final
class DeleteImageCommandHandler:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        image_storage: ImageStorage,
        user_command_gateway: UserCommandGateway,
        transaction_manager: TransactionManager,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._image_storage: Final[ImageStorage] = image_storage
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: DeleteImageCommand) -> None:
        logger.info(
            "Started deleting image with id: %s",
            data.image_id,
        )

        logger.info("Started getting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user: %s", current_user)

        typed_image_id: ImageID = cast("ImageID", data.image_id)

        logger.info("Started searching for image with id: %s", typed_image_id)
        image: Image | None = await self._image_storage.read_by_id(typed_image_id)

        if image is None:
            msg = f"Image with id: {typed_image_id} not found"
            raise ImageNotFoundError(msg)

        logger.info("Successfully found image with id: %s", image)

        if typed_image_id not in current_user.images:
            msg = "Photo with id: %s doesn't belong to current user"
            raise ImageDoesntBelongToThisUserError(msg)

        current_user.images.remove(typed_image_id)
        logger.info("Removing image with id: %s from image storage", typed_image_id)
        await self._image_storage.delete_by_id(typed_image_id)
        logger.info("Successfully removed image with id: %s from image storage", typed_image_id)
        logger.info("Started deleting image: %s from user entity: %s", typed_image_id, current_user.id)
        await self._user_command_gateway.update(current_user)

        await self._transaction_manager.flush()
        await self._transaction_manager.commit()

        logger.info("Successfully deleted image with id: %s", typed_image_id)
