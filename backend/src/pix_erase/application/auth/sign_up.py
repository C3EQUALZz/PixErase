import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.auth.sign_up import SignUpView
from pix_erase.application.consts import AUTH_ALREADY_AUTHENTICATED
from pix_erase.application.errors.auth import AlreadyAuthenticatedError, AuthenticationError
from pix_erase.application.errors.user import UserAlreadyExistsError
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.raw_password import RawPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_name import Username
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpData:
    email: str
    name: str
    password: str
    role: UserRole = UserRole.USER


@final
class SignUpHandler:
    """
    - Open to everyone.
    - Registers a new user with validation and uniqueness checks.
    - Passwords are peppered, salted, and stored as hashes.
    - A logged-in user cannot sign up until the session expires or is terminated.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_service: UserService,
        user_command_gateway: UserCommandGateway,
        transaction_manager: TransactionManager,
        event_bus: EventBus,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_service: Final[UserService] = user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._event_bus: Final[EventBus] = event_bus

    async def __call__(self, data: SignUpData) -> SignUpView:
        logger.info("Sign up: started. Username: '%s'.", data.name)

        try:
            await self._current_user_service.get_current_user()
            raise AlreadyAuthenticatedError(AUTH_ALREADY_AUTHENTICATED)
        except AuthenticationError:
            pass

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

        return SignUpView(
            user_id=new_user.id,
        )
