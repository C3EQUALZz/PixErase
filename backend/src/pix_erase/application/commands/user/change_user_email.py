import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.authorization.composite import AnyOf
from pix_erase.domain.user.services.authorization.permission import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext
)
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserEmailCommand:
    user_id: UUID
    new_email: str


@final
class ChangeUserEmailCommandHandler:
    """
    - Open to authenticated users.
    - Changes user email.
    - Current user can update himself from system.
    - Admins can update email of subordinate users.
    """

    def __init__(
            self,
            transaction_manager: TransactionManager,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            current_user_service: CurrentUserService,
            event_bus: EventBus,
            access_service: AccessService,
    ) -> None:
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._event_bus: Final[EventBus] = event_bus
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: ChangeUserEmailCommand) -> None:
        logger.info("Change user email started.")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Read current user identified. User ID: '%s'.", current_user.id)

        user_for_update_email: User | None = await self._user_command_gateway.read_by_id(
            user_id=UserID(data.user_id),
        )

        if user_for_update_email is None:
            msg: str = f"Cant find user by ID: {data.user_id}"
            raise UserNotFoundByIDError(msg)

        self._access_service.authorize(
            AnyOf(
                CanManageSelf(),
                CanManageSubordinate(),
            ),
            context=UserManagementContext(
                subject=current_user,
                target=user_for_update_email,
            )
        )

        validated_email: UserEmail = UserEmail(data.new_email)
        self._user_service.change_email(user_for_update_email, validated_email)

        await self._event_bus.publish(self._user_service.pull_events())
        await self._transaction_manager.commit()
        logger.info("Change user email completed.")
