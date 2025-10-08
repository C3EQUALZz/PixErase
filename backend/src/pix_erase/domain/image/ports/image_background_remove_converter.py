from typing import Protocol
from abc import abstractmethod


class ImageRemoveBackgroundConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes) -> bytes:
        ...
