from abc import abstractmethod
from typing import NewType, Literal
from typing import Protocol

from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_scale import ImageScale

TaskID = NewType('TaskID', str)


class ImageTaskManager(Protocol):
    @abstractmethod
    async def convert_to_grayscale(self, image_id: ImageID) -> TaskID:
        ...

    @abstractmethod
    async def compress(self, image_id: ImageID, quality: int) -> TaskID:
        ...

    @abstractmethod
    async def rotate(self, image_id: ImageID, angle: int) -> TaskID:
        ...

    @abstractmethod
    async def upscale(
            self,
            image_id: ImageID,
            algorithm: Literal["AI", "NearestNeighbour"],
            scale: ImageScale
    ) -> TaskID:
        ...
