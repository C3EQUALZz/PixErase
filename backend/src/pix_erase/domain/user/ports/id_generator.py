from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.user.values.user_id import UserID


class UserIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> UserID:
        raise NotImplementedError
