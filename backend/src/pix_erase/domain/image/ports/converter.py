from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.image.entities.image import Image


class ImageConverter(Protocol):
    @abstractmethod
    def convert(self, image: Image) -> Image:
        ...
