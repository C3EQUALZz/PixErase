import logging
from dataclasses import dataclass
from typing import final, Final

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_params.pagination import Pagination
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserQueryFilters, UserListParams, UserListSorting
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.application.errors.query_params import SortingError
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.services.access_service import AccessService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadAllUsersQuery:
    limit: int
    offset: int
    sorting_field: str
    sorting_order: SortingOrder


@final
class ReadAllUsersQueryHandler:
    """
    - Open to everyone.
    - Retrieves a paginated list of existing users with relevant information.
    """

    def __init__(
            self,
            user_query_gateway: UserQueryGateway,
            current_user_service: CurrentUserService,
            access_service: AccessService,
    ) -> None:
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._current_user_service: Final[CurrentUserService] = current_user_service
        self._access_service: Final[AccessService] = access_service

    async def __call__(self, data: ReadAllUsersQuery) -> list[ReadUserByIDView]:
        logger.info("List users started")

        logger.debug("Started got current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.debug("Got current user, user id: %s", current_user.id)

        logger.debug("Retrieving list of users.")

        user_list_params: UserListParams = UserListParams(
            pagination=Pagination(
                limit=data.limit,
                offset=data.offset,
            ),
            sorting=UserListSorting(
                sorting_field=UserQueryFilters(data.sorting_field),
                sorting_order=data.sorting_order,
            ),
        )

        users: list[User] | None = await self._user_query_gateway.read_all_users(
            user_list_params
        )

        if users is None:
            logger.error(
                "Retrieving list of users failed: invalid sorting column '%s'.",
                data.sorting_field,
            )
            msg = f"Invalid sorting field: {data.sorting_field}"
            raise SortingError(msg)

        response: list[ReadUserByIDView] = [
            ReadUserByIDView(
                id=user.id,
                email=str(user.email),
                name=str(user.name),
                role=user.role
            )
            for user in users
        ]

        return response
