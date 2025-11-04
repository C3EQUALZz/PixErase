from abc import abstractmethod
from typing import Protocol


class ImageResizerConverter(Protocol):
    @abstractmethod
    def resize(self, data: bytes, image_width: int, image_height: int) -> bytes: ...
