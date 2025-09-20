from abc import abstractmethod
from typing import Protocol

from pix_erase.application.common.query_params.user_filters import UserListParams
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_id import UserID


class UserQueryGateway(Protocol):
    @abstractmethod
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        ...
