from abc import abstractmethod
from typing import Protocol, TypedDict


class ScoresDTO(TypedDict):
    CORREL: float
    CHISQR: float
    INTERSECT: float
    BHATTACHARYYA: float
    MSE: float  # Mean Squared Error
    PSNR: float  # Peak Signal-to-Noise Ratio
    SSIM: float  # Structural Similarity Index


class ImageComparerConverter(Protocol):
    @abstractmethod
    def compare_by_histograms(self, first_image: bytes, second_image: bytes) -> ScoresDTO:
        ...
