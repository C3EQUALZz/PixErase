import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.image.extractor import ImageInfo, ImageInfoExtractor
from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.image.create_image import CreateImageView
from pix_erase.domain.image.services.image_service import ImageService
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize
from pix_erase.domain.user.services.user_service import UserService

if TYPE_CHECKING:
    from pix_erase.domain.image.entities.image import Image
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateImageCommand:
    data: bytes
    filename: str


@final
class CreateImageCommandHandler:
    """
    - Opens to everyone
    - Creates image in system for future processing
    - In first step we must save image and use index for here to processing
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        image_storage: ImageStorage,
        image_extractor: ImageInfoExtractor,
        image_service: ImageService,
        user_service: UserService,
        transaction_manager: TransactionManager,
        user_command_gateway: UserCommandGateway,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._image_storage: Final[ImageStorage] = image_storage
        self._image_extractor: Final[ImageInfoExtractor] = image_extractor
        self._image_service: Final[ImageService] = image_service
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway

    async def __call__(self, data: CreateImageCommand) -> CreateImageView:
        logger.info("Started creating new image in system with filename: %s", data.filename)

        logger.info("Getting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Current user is: %s", current_user.id)

        logger.info("Started getting metadata from image with name: %s", data.filename)
        metadata_from_image: ImageInfo = await self._image_extractor.extract(data=data.data)
        logger.info("Successfully got metadata from image with name: %s", data.filename)

        logger.info("Creating a new image entity with name: %s", data.filename)
        new_image: Image = self._image_service.create(
            image_name=ImageName(data.filename),
            image_height=ImageSize(metadata_from_image.height),
            image_width=ImageSize(metadata_from_image.width),
            data=data.data,
        )
        logger.info("Got index for new image entity: %s with name: %s", new_image.id, new_image.name)

        logger.info("Started adding image with id: %s to storage", new_image.id)
        await self._image_storage.add(image=new_image)
        logger.info("Successfully added into storage new image entity with id: %s", new_image.id)

        self._user_service.add_image(user=current_user, image=new_image)

        logger.info("Added image to user: %s, images from this user: %s", current_user.id, current_user.images)

        await self._user_command_gateway.update(user=current_user)
        await self._transaction_manager.flush()
        await self._transaction_manager.commit()

        view: CreateImageView = CreateImageView(image_id=new_image.id)

        logger.info("Finished adding image with id: %s", new_image.id)

        return view
