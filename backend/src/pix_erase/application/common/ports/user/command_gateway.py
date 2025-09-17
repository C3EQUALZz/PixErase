from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID


class UserCommandGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def exists_with_email(self, email: UserEmail) -> bool: ...

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> User | None: ...

    @abstractmethod
    async def read_by_email(self, email: UserEmail) -> User | None: ...

    @abstractmethod
    async def delete_by_id(self, user_id: UserID) -> None: ...