import re
from dataclasses import dataclass
from email.utils import parseaddr
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.user.errors.user import WrongUserAccountEmailFormatError

EMAIL_REGEX_COMPILED_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class UserEmail(BaseValueObject):
    """
    Represents an email address

    This value object doesn't check if email is real, only check syntax.
    """

    value: str

    @override
    def _validate(self) -> None:
        if not EMAIL_REGEX_COMPILED_PATTERN.fullmatch(self.value) or not parseaddr(self.value)[1]:
            msg = "Please provide a valid email address"
            raise WrongUserAccountEmailFormatError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)