from abc import abstractmethod
from typing import Protocol


class ImageColorToCrayScaleConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes) -> bytes: ...
