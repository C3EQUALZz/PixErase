import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.user.create_user import CreateUserView
from pix_erase.application.errors.user import UserAlreadyExistsError
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.authorization.permission import CanManageRole, RoleManagementContext
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.raw_password import RawPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_name import Username
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserCommand:
    email: str
    name: str
    password: str
    role: UserRole = UserRole.USER


@final
class CreateUserCommandHandler:
    def __init__(
            self,
            transaction_manager: TransactionManager,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            event_bus: EventBus,
            current_user_service: CurrentUserService,
            access_service: AccessService,
    ) -> None:
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._event_bus: Final[EventBus] = event_bus
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: CreateUserCommand) -> CreateUserView:
        logger.info(
            "Create user: started. Username: '%s'.",
            data.name,
        )

        current_user: User = await self._current_user_service.get_current_user()

        self._access_service.authorize(
            CanManageRole(),
            context=RoleManagementContext(
                subject=current_user,
                target_role=data.role,
            ),
        )

        new_user: User = self._user_service.create(
            email=UserEmail(data.email),
            name=Username(data.name),
            raw_password=RawPassword(data.password),
            role=data.role,
        )

        if (await self._user_command_gateway.read_by_email(new_user.email)) is not None:
            msg: str = f"user with this email: {new_user.email} already exists"
            raise UserAlreadyExistsError(msg)

        await self._user_command_gateway.add(new_user)
        await self._transaction_manager.flush()
        await self._event_bus.publish(self._user_service.pull_events())
        await self._transaction_manager.commit()

        logger.info("Create user: done. Username: '%s'.", new_user.name)

        return CreateUserView(
            user_id=new_user.id,
        )
