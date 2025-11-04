from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.image.values.image_id import ImageID


class ImageIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> ImageID: ...
