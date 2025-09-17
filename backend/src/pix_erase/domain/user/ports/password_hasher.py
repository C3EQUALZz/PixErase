from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.user.values.hashed_password import HashedPassword
from pix_erase.domain.user.values.raw_password import RawPassword


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, raw_password: RawPassword) -> HashedPassword:
        raise NotImplementedError

    @abstractmethod
    def verify(self, *, raw_password: RawPassword, hashed_password: HashedPassword) -> bool:
        raise NotImplementedError