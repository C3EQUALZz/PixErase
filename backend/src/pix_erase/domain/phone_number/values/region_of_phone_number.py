from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.phone_number.errors.region_of_phone_number import (
    EmptyRegionOfPhoneNumberError,
    InvalidRegionOfPhoneNumberLengthError,
)

MAX_REGION_LENGTH: Final[int] = 200


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class RegionOfPhoneNumber(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if not self.value or self.value.isspace():
            msg = "Region cannot be empty"
            raise EmptyRegionOfPhoneNumberError(msg)

        if len(self.value) > MAX_REGION_LENGTH:
            msg = f"Region name too long. Maximum length is {MAX_REGION_LENGTH} characters"
            raise InvalidRegionOfPhoneNumberLengthError(msg)

    @override
    def __str__(self) -> str:
        return self.value
