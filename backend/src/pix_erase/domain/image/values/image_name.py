import re
from dataclasses import dataclass
from typing import Final

from typing_extensions import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.image.errors.image import BadImageNameError

IGNORE_RUSSIAN_LETTERS_PATTERN: Final[re.Pattern[str]] = re.compile("^[а-яА-ЯЁё]")


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ImageName(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if self.value == "" or self.value.isspace():
            msg = f"{self.value} is empty"
            raise BadImageNameError(msg)

        if IGNORE_RUSSIAN_LETTERS_PATTERN.search(self.value):
            msg = f"{self.value} is illegal, please provide without russian letters"
            raise BadImageNameError(msg)

    @override
    def __str__(self) -> str:
        return self.value
