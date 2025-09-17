from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.user.errors.user import PasswordCantBeEmptyError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class HashedPassword(BaseValueObject):
    value: bytes

    @override
    def _validate(self) -> None:
        if self.value == b"":
            msg = "Please enter a password"
            raise PasswordCantBeEmptyError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)