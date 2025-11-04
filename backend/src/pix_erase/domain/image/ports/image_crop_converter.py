from abc import abstractmethod
from typing import Protocol


class ImageCropConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes, new_width: int, new_height: int) -> bytes: ...
