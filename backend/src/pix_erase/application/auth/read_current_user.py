import logging
from typing import final, Final

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.services.auth_session import AuthSessionService
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.services.user_service import UserService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class ReadCurrentUserHandler:
    """
    - Opens to everyone.
    - Get current user, extracting info from cookie.
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_command_gateway: UserQueryGateway,
            user_service: UserService,
            auth_session_service: AuthSessionService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_command_gateway: Final[UserQueryGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._auth_session_service: Final[AuthSessionService] = auth_session_service

    async def __call__(self) -> ReadUserByIDView:
        logger.info("Read current user started.")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Read current user identified. User ID: '%s'.", current_user.id)

        view: ReadUserByIDView = ReadUserByIDView(
            id=current_user.id,
            email=str(current_user.email),
            name=str(current_user.name),
            role=current_user.role,
        )

        logger.info("Read current user ended successfully.")
        return view
