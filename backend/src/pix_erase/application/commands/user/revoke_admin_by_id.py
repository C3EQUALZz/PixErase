import logging
from dataclasses import dataclass
from typing import Final, final
from uuid import UUID

from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.authorization.permission import CanManageRole, RoleManagementContext
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_role import UserRole

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RevokeAdminByIDCommand:
    user_id: UUID


@final
class RevokeAdminByIDCommandHandler:
    """
    - Open to super admins.
    - Revokes admin rights from a specified user.
    - Super admin rights can not be changed
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            transaction_manager: TransactionManager,
            access_service: AccessService,
            event_bus: EventBus,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._access_service: Final[AccessService] = access_service
        self._event_bus: Final[EventBus] = event_bus

    async def __call__(self, data: RevokeAdminByIDCommand) -> None:
        logger.info(
            "Revoke admin: started. User id: '%s'.",
            data.user_id,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._access_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=UserRole.ADMIN,
            ),
        )

        user_for_revoke_admin: User | None = await self._user_command_gateway.read_by_id(
            user_id=UserID(data.user_id),
        )

        if user_for_revoke_admin is None:
            msg: str = f"Cant find user by ID: {data.user_id}"
            raise UserNotFoundByIDError(msg)

        self._access_service.toggle_user_admin_role(user_for_revoke_admin, is_admin=False)
        await self._event_bus.publish(self._access_service.pull_events())
        await self._transaction_manager.commit()

        logger.info(
            "Revoke admin: done. User id: '%s'.",
            data.user_id,
        )
