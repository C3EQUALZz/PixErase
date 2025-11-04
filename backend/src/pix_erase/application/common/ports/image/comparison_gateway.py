from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.image.entities.image_comparison import ImageComparison
from pix_erase.domain.image.values.comparison_id import ComparisonID
from pix_erase.domain.image.values.image_id import ImageID


class ImageComparisonGateway(Protocol):
    @abstractmethod
    async def add(self, comparison: ImageComparison) -> None:
        """Save image comparison result."""
        ...

    @abstractmethod
    async def read_by_id(self, comparison_id: ComparisonID) -> ImageComparison | None:
        """Read comparison by ID."""
        ...

    @abstractmethod
    async def read_by_image_ids(
        self,
        first_image_id: ImageID,
        second_image_id: ImageID,
    ) -> ImageComparison | None:
        """Read comparison by image IDs (order-independent)."""
        ...
