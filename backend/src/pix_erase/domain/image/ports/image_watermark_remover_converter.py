from typing import Protocol
from abc import abstractmethod


class ImageWatermarkRemoverConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes) -> bytes:
        ...
