from abc import abstractmethod
from typing import Protocol


class ImageRemoveBackgroundConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes) -> bytes: ...
