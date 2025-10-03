from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID


class ImageStorage(Protocol):
    @abstractmethod
    async def add(self, image: Image) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, image_id: ImageID) -> Image:
        ...

    @abstractmethod
    async def delete_by_id(self, image_id: ImageID) -> None:
        ...

    @abstractmethod
    async def update(self, image: Image) -> None:
        ...
