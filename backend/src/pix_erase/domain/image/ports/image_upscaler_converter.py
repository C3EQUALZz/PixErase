from abc import abstractmethod
from typing import Protocol


class ImageUpscaleConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes, width: int, height: int) -> bytes:
        ...
