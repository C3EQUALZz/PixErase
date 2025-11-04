from dataclasses import dataclass

from pix_erase.domain.image.ports.image_comparer_converter import ScoresDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class CompareImageView:
    """View for image comparison results."""

    scores: ScoresDTO
    different_names: bool
    different_width: bool
    different_height: bool
