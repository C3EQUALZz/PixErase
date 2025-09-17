from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.user.errors.raw_password import (
    EmptyPasswordWasProvidedError,
    WeakPasswordWasProvidedError,
)

MIN_PASSWORD_LENGTH: Final[int] = 8
MAX_PASSWORD_LENGTH: Final[int] = 255


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class RawPassword(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value.isspace() or self.value == "":
            msg = "Please enter a password with digits and alphas, not empty string"
            raise EmptyPasswordWasProvidedError(msg)

        if self.value.isdigit():
            msg = "Please enter password with digits and alphas, not only digits"
            raise WeakPasswordWasProvidedError(msg)

        if len(self.value) < MIN_PASSWORD_LENGTH:
            msg = "Password too short. Please provide bigger than 8 characters"
            raise WeakPasswordWasProvidedError(msg)

        if len(self.value) > MAX_PASSWORD_LENGTH:
            msg = "Password too long. Please provide less than 255 characters"
            raise WeakPasswordWasProvidedError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
