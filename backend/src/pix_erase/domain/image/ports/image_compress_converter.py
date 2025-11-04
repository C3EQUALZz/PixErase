from abc import abstractmethod
from typing import Protocol


class ImageCompressConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes, quality: int = 90) -> bytes: ...
