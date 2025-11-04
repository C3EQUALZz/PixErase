import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.services.auth_session import AuthSessionService
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.consts import (
    AUTH_ACCOUNT_INACTIVE,
    AUTH_ALREADY_AUTHENTICATED,
    AUTH_INVALID_PASSWORD,
    USER_NOT_FOUND,
)
from pix_erase.application.errors.auth import AlreadyAuthenticatedError, AuthenticationError
from pix_erase.application.errors.user import UserNotFoundByEmailError
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.raw_password import RawPassword
from pix_erase.domain.user.values.user_email import UserEmail

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class LogInData:
    email: str
    password: str


@final
class LogInHandler:
    """
    - Open to everyone.
    - Authenticates registered user,
    sets a JWT access token with a session ID in cookies,
    and creates a session.
    - A logged-in user cannot log in again
    until the session expires or is terminated.
    - Authentication renews automatically
    when accessing protected routes before expiration.
    - If the JWT is invalid, expired, or the session is terminated,
    the user loses authentication.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        user_command_gateway: UserCommandGateway,
        user_service: UserService,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._auth_session_service: Final[AuthSessionService] = auth_session_service

    async def __call__(self, data: LogInData) -> None:
        logger.info("Log in: started. Email: '%s'.", data.email)

        try:
            await self._current_user_service.get_current_user()
            raise AlreadyAuthenticatedError(AUTH_ALREADY_AUTHENTICATED)
        except AuthenticationError:
            pass

        email: UserEmail = UserEmail(data.email)
        password: RawPassword = RawPassword(data.password)

        user: User | None = await self._user_command_gateway.read_by_email(email)
        if user is None:
            msg: str = f"{USER_NOT_FOUND}: {email}"
            raise UserNotFoundByEmailError(msg)

        if not self._user_service.is_password_valid(user, password):
            raise AuthenticationError(AUTH_INVALID_PASSWORD)

        if not user.is_active:
            raise AuthenticationError(AUTH_ACCOUNT_INACTIVE)

        await self._auth_session_service.create_session(user.id)

        logger.info(
            "Log in: done. User, ID: '%s', username '%s', role '%s'.",
            user.id,
            user.email,
            user.role.value,
        )
