import re
from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.phone_number.errors.raw_phone_number import (
    EmptyRawPhoneNumberError,
    InvalidRawPhoneNumberFormatError,
)

# Pattern allows: digits, spaces, plus, parentheses, hyphens, and dots
PHONE_NUMBER_ALLOWED_CHARS_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[0-9+\-()\s.]+$")
MIN_PHONE_NUMBER_LENGTH: Final[int] = 3
MAX_PHONE_NUMBER_LENGTH: Final[int] = 20


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class RawPhoneNumber(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if not self.value or self.value.isspace():
            msg = "Phone number cannot be empty"
            raise EmptyRawPhoneNumberError(msg)

        if len(self.value) < MIN_PHONE_NUMBER_LENGTH:
            msg = f"Phone number too short. Minimum length is {MIN_PHONE_NUMBER_LENGTH} characters"
            raise InvalidRawPhoneNumberFormatError(msg)

        if len(self.value) > MAX_PHONE_NUMBER_LENGTH:
            msg = f"Phone number too long. Maximum length is {MAX_PHONE_NUMBER_LENGTH} characters"
            raise InvalidRawPhoneNumberFormatError(msg)

        if not PHONE_NUMBER_ALLOWED_CHARS_PATTERN.match(self.value):
            msg = "Phone number contains invalid characters. Only digits, spaces, +, -, (, ), and . are allowed"
            raise InvalidRawPhoneNumberFormatError(msg)

        # Check that there's at least one digit
        if not any(char.isdigit() for char in self.value):
            msg = "Phone number must contain at least one digit"
            raise InvalidRawPhoneNumberFormatError(msg)

    @override
    def __str__(self) -> str:
        return self.value
