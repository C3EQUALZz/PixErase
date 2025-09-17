import logging
from typing import TYPE_CHECKING, Final

from pix_erase.application.common.ports.access_revoker import AccessRevoker
from pix_erase.application.common.ports.identity_provider import IdentityProvider
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.domain.user.errors.access_service import AuthorizationError
from pix_erase.domain.user.entities.user import User

if TYPE_CHECKING:
    from pix_erase.domain.user.values.user_id import UserID

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CurrentUserService:
    def __init__(
            self,
            identity_provider: IdentityProvider,
            user_command_gateway: UserCommandGateway,
            access_revoker: AccessRevoker,
    ) -> None:
        self._identity_provider: Final[IdentityProvider] = identity_provider
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._access_revoker: Final[AccessRevoker] = access_revoker
        self._cached_current_user: User | None = None

    async def get_current_user(self) -> User:
        if self._cached_current_user is not None:
            return self._cached_current_user

        current_user_id: UserID = await self._identity_provider.get_current_user_id()
        user: User | None = await self._user_command_gateway.read_by_id(current_user_id)

        if user is None:
            logger.warning("Failed to retrieve current user. Removing all access. ID: %s.", current_user_id)

            await self._access_revoker.remove_all_user_access(current_user_id)
            msg = "Not authorized."
            raise AuthorizationError(msg)

        self._cached_current_user = user
        return user
