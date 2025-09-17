import logging
from typing import TYPE_CHECKING, Final, final

from automatic_responses.application.common.services.current_user import CurrentUserService
from automatic_responses.infrastructure.auth.session.service import AuthSessionService

if TYPE_CHECKING:
    from automatic_responses.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class LogOutHandler:
    """
    - Open to authenticated users.
    - Logs the user out by deleting the JWT access token from cookies
    and removing the session from the database.
    """

    def __init__(
        self,
        current_user_service: CurrentUserService,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._auth_session_service: Final[AuthSessionService] = auth_session_service

    async def __call__(self) -> None:
        """
        :raises AuthenticationError:
        :raises RepoError:
        :raises AuthorizationError:
        """
        logger.info("Log out: started for unknown user.")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Log out: user identified. User ID: '%s'.", current_user.id)
        await self._auth_session_service.invalidate_current_session()
        logger.info("Log out: done. User ID: '%s'.", current_user.id)