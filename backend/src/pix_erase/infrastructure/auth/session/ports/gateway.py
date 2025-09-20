from abc import abstractmethod
from typing import Protocol

from automatic_responses.domain.user.values.user_id import UserID
from automatic_responses.infrastructure.auth.session.model import AuthSession


class AuthSessionGateway(Protocol):
    """
    Defined to allow easier mocking and swapping
    of implementations in the same layer.
    """

    @abstractmethod
    def add(self, auth_session: AuthSession) -> None:
        """
        :raises DataMapperError:
        """

    @abstractmethod
    async def read_by_id(self, auth_session_id: str) -> AuthSession | None:
        """
        :raises DataMapperError:
        """

    @abstractmethod
    async def update(self, auth_session: AuthSession) -> None:
        """
        :raises DataMapperError:
        """

    @abstractmethod
    async def delete(self, auth_session_id: str) -> None:
        """
        :raises DataMapperError:
        """

    @abstractmethod
    async def delete_all_for_user(self, user_id: UserID) -> None:
        """
        :raises DataMapperError:
        """