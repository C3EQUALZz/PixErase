from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.phone_number.errors.operator_of_phone_number import (
    EmptyOperatorOfPhoneNumberError,
    InvalidOperatorOfPhoneNumberLengthError,
)

MAX_OPERATOR_LENGTH: Final[int] = 100


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class OperatorOfPhoneNumber(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if not self.value or self.value.isspace():
            msg = "Operator name cannot be empty"
            raise EmptyOperatorOfPhoneNumberError(msg)

        if len(self.value) > MAX_OPERATOR_LENGTH:
            msg = f"Operator name too long. Maximum length is {MAX_OPERATOR_LENGTH} characters"
            raise InvalidOperatorOfPhoneNumberLengthError(msg)

    @override
    def __str__(self) -> str:
        return self.value
