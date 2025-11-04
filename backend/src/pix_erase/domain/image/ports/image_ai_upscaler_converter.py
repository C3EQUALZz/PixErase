from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.image.values.image_scale import ImageScale


class ImageAIUpscaleConverter(Protocol):
    @abstractmethod
    def convert(self, data: bytes, width: int, height: int, scale: ImageScale) -> bytes: ...
