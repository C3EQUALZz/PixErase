import re
from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.user.errors.user import (
    TooBigUserAccountNameError,
    UserAccountNameCantBeEmptyError,
    TooSmallUserAccountNameError, BadUserNameError
)

MAX_LENGTH_OF_USERNAME: Final[int] = 255
MIN_LENGTH_OF_USERNAME: Final[int] = 2

# - starts with a letter (A-Z, a-z) or a digit (0-9)
PATTERN_START: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9]",
)
# - can contain multiple special characters . - _ between letters and digits,
PATTERN_ALLOWED_CHARS: Final[re.Pattern[str]] = re.compile(
    r"[a-zA-Z0-9._-]*",
)
#   but only one special character can appear consecutively
PATTERN_NO_CONSECUTIVE_SPECIALS: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$",
)
# - ends with a letter (A-Z, a-z) or a digit (0-9)
PATTERN_END: Final[re.Pattern[str]] = re.compile(
    r".*[a-zA-Z0-9]$",
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Username(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value.isspace() or self.value == "":
            msg = "Please provide a non-empty user account name"
            raise UserAccountNameCantBeEmptyError(msg)

        if len(self.value) > MAX_LENGTH_OF_USERNAME:
            msg = "Please provide a name less than 255 characters"
            raise TooBigUserAccountNameError(msg)

        if len(self.value) < MIN_LENGTH_OF_USERNAME:
            msg = "Please provide a name more than 2 characters"
            raise TooSmallUserAccountNameError(msg)

        if not re.match(PATTERN_START, self.value):
            msg = "Username must start with a letter (A-Z, a-z) or a digit (0-9)."
            raise BadUserNameError(msg)

        if not re.fullmatch(PATTERN_ALLOWED_CHARS, self.value):
            msg = (
                "Username can only contain letters (A-Z, a-z), digits (0-9), "
                "dots (.), hyphens (-), and underscores (_)."
            )
            raise BadUserNameError(msg)

        if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, self.value):
            msg = (
                "Username cannot contain consecutive special characters"
                " like .., --, or __."
            )

            raise BadUserNameError(msg)

        if not re.match(PATTERN_END, self.value):
            msg = "Username must end with a letter (A-Z, a-z) or a digit (0-9)."
            raise BadUserNameError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
