from typing import Final

from pix_erase.application.common.ports.access_revoker import AccessRevoker
from pix_erase.application.common.services.auth_session import AuthSessionService
from pix_erase.domain.user.values.user_id import UserID


class AuthSessionAccessRevoker(AccessRevoker):
    def __init__(
            self,
            auth_session_service: AuthSessionService,
    ) -> None:
        self._auth_session_service: Final[AuthSessionService] = auth_session_service

    async def remove_all_user_access(self, user_id: UserID) -> None:
        """
        :raises DataMapperError:
        """
        await self._auth_session_service.invalidate_all_sessions_for_user(user_id)
