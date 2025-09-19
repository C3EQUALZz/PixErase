from dataclasses import dataclass

from typing_extensions import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.image.errors.image import NumberCannotBeNegativeError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageSize(BaseValueObject):
    value: int

    @override
    def _validate(self) -> None:
        if self.value <= 0:
            msg = f"{self.value} is negative"
            raise NumberCannotBeNegativeError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
