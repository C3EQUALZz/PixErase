from dataclasses import dataclass

from pix_erase.domain.image.ports.image_comparer_converter import ScoresDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ImageComparisonResult:
    """Result of comparing two images."""
    scores: ScoresDTO
    different_names: bool
    different_width: bool
    different_height: bool
