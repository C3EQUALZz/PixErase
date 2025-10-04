from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from pix_erase.domain.common.values.base import BaseValueObject

ImageID = NewType("ImageID", UUID)

# @dataclass(frozen=True, eq=True, unsafe_hash=True)
# class ImageID(BaseValueObject):
#     value: UUID
#
#     def _validate(self) -> None:
#         ...
#
#     def __str__(self) -> str:
#         return str(self.value)
