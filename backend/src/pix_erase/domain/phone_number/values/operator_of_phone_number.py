from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class OperatorOfPhoneNumber(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None: ...

    @override
    def __str__(self) -> str:
        return self.value
