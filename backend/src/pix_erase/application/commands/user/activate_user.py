import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final
from uuid import UUID

from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.authorization.permission import (
    CanManageRole,
    CanManageSubordinate,
    RoleManagementContext,
    UserManagementContext,
)
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ActivateUserCommand:
    user_id: UUID


@final
class ActivateUserCommandHandler:
    """
    - Open to admins.
    - Restores a previously soft-deleted user.
    - Only super admins can activate other admins.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_command_gateway: UserCommandGateway,
        user_service: UserService,
        transaction_manager: TransactionManager,
        access_service: AccessService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: ActivateUserCommand) -> None:
        logger.info(
            "Activate user: started. Username: '%s'.",
            data.user_id,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._access_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.USER,
            ),
        )

        user_for_activation: User | None = await self._user_command_gateway.read_by_id(
            user_id=UserID(data.user_id),
        )

        if user_for_activation is None:
            msg: str = f"Can't find user by ID: {data.user_id}"
            raise UserNotFoundByIDError(msg)

        self._access_service.authorize(
            CanManageSubordinate(),
            context=UserManagementContext(
                subject=current_user,
                target=user_for_activation,
            ),
        )

        self._access_service.toggle_user_activation(user_for_activation, is_active=True)
        await self._transaction_manager.commit()

        logger.info(
            "Activate user: done. Username: '%s'.",
            user_for_activation.id,
        )
