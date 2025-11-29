import re
from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.phone_number.errors.timezone_of_phone_number import (
    EmptyTimezoneOfPhoneNumberError,
    InvalidTimezoneOfPhoneNumberFormatError,
)

TIMEZONE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(UTC|GMT)[+-]\d{1,2}(:\d{2})?$|^[A-Z][a-z]+/[A-Za-z_]+$",
    re.IGNORECASE,
)
MAX_TIMEZONE_LENGTH: Final[int] = 50


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class TimezoneOfPhoneNumber(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if not self.value or self.value.isspace():
            msg = "Timezone cannot be empty"
            raise EmptyTimezoneOfPhoneNumberError(msg)

        if len(self.value) > MAX_TIMEZONE_LENGTH:
            msg = f"Timezone too long. Maximum length is {MAX_TIMEZONE_LENGTH} characters"
            raise InvalidTimezoneOfPhoneNumberFormatError(msg)

        if not TIMEZONE_PATTERN.match(self.value):
            msg = (
                "Invalid timezone format. Expected format: 'UTC±HH:MM', 'GMT±HH:MM', "
                "or 'Continent/City' (e.g., 'Europe/Moscow')"
            )
            raise InvalidTimezoneOfPhoneNumberFormatError(msg)

    @override
    def __str__(self) -> str:
        return self.value
