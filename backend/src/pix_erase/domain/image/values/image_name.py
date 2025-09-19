from dataclasses import dataclass
from typing_extensions import override
from pix_erase.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value == "" or self.value.isspace():
            raise WrongTypeError(f"{self.value} is empty")

    @override
    def __str__(self) -> str:
        return self.value
