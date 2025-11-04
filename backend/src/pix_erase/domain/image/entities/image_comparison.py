from dataclasses import dataclass

from pix_erase.domain.common.entities.base_aggregate import BaseAggregateRoot
from pix_erase.domain.image.ports.image_comparer_converter import ScoresDTO
from pix_erase.domain.image.values.comparison_id import ComparisonID
from pix_erase.domain.image.values.image_id import ImageID


@dataclass(eq=False)
class ImageComparison(BaseAggregateRoot[ComparisonID]):
    """Entity representing a comparison result between two images."""

    first_image_id: ImageID
    second_image_id: ImageID
    scores: ScoresDTO
    different_names: bool
    different_width: bool
    different_height: bool
