from dataclasses import dataclass
from typing import override

from automatic_responses.domain.common.values.base import BaseValueObject
from automatic_responses.domain.user.errors.user import PasswordCantBeEmptyError


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