from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.image.errors.image import BadImageUpscaleAlgorithmError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageUpscaleAlgorithm(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value not in ("AI", "NearestNeighbour"):
            msg = f"{self.value} is not a valid value"
            raise BadImageUpscaleAlgorithmError(msg)

    @override
    def __str__(self) -> str:
        return self.value
