from typing import Protocol
from abc import abstractmethod

class ImageResizerConverter(Protocol):
    @abstractmethod
    def resize(self, data: bytes, image_width: int, image_height: int) -> bytes:
        ...
