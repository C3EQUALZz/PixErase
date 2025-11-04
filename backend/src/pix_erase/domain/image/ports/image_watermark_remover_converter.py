from abc import abstractmethod
from typing import Protocol


class ImageWatermarkRemoverConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes) -> bytes: ...
