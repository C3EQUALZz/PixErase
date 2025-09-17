from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.user.errors.user import TooBigUserAccountNameError, UserAccountNameCantBeEmptyError

MAX_LENGTH_OF_USERNAME: Final[int] = 255


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

    @override
    def __str__(self) -> str:
        return str(self.value)