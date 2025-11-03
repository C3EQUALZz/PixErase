import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final
from uuid import UUID

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.authorization.composite import AnyOf
from pix_erase.domain.user.services.authorization.permission import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext
)
from pix_erase.domain.user.values.user_id import UserID

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadUserByIDQuery:
    user_id: UUID


@final
class ReadUserByIDQueryHandler:
    """
    - Open to everyone.
    - Finds user by unique ID in system.
    """

    def __init__(
            self,
            current_user_service: CurrentUserService,
            user_query_gateway: UserQueryGateway,
            access_service: AccessService,
    ) -> None:
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: ReadUserByIDQuery) -> ReadUserByIDView:
        logger.info("Get user by id started, user_id: %s", data.user_id)

        current_user: User = await self._current_user_service.get_current_user()

        user_id: UserID = UserID(data.user_id)

        user: User | None = await self._user_query_gateway.read_user_by_id(user_id)

        if user is None:
            msg: str = f"Can't find user by id: {data.user_id}"
            raise UserNotFoundByIDError(msg)

        self._access_service.authorize(
            AnyOf(
                CanManageSelf(),
                CanManageSubordinate(),
            ),
            context=UserManagementContext(
                subject=current_user,
                target=user,
            ),
        )

        logger.info("Read user by id: done.")

        return ReadUserByIDView(
            id=user_id,
            email=str(user.email),
            name=str(user.name),
            role=user.role,
        )
