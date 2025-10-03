from abc import abstractmethod
from typing import NewType
from typing import Protocol

from pix_erase.domain.image.values.image_id import ImageID

TaskID = NewType('TaskID', str)


class ImageTaskManager(Protocol):
    @abstractmethod
    async def convert_to_grayscale(self, image_id: ImageID) -> TaskID:
        ...

    @abstractmethod
    async def compress(self, image_id: ImageID) -> TaskID:
        ...
