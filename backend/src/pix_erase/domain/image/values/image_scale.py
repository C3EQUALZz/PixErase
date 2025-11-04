from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.image.errors.image import BadImageScaleError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageScale(BaseValueObject):
    value: int

    @override
    def _validate(self) -> None:
        if self.value not in (2, 3, 4):
            msg = f"Scale factor must be 2, 3, or 4, not another {self.value}"
            raise BadImageScaleError(msg)

    @override
    def __str__(self) -> str:
        return str(self.value)
