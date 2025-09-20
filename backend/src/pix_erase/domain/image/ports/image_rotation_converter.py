from abc import abstractmethod
from typing import Protocol


class ImageRotationConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes, angle: int = 90) -> bytes:
        ...
