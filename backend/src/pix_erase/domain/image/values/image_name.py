from dataclasses import dataclass
from typing_extensions import override
from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.image.errors.image import BadImageNameError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value == "" or self.value.isspace():
            msg = f"{self.value} is empty"
            raise BadImageNameError(msg)

    @override
    def __str__(self) -> str:
        return self.value
