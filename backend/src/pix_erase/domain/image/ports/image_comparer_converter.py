from abc import abstractmethod
from typing import Protocol, TypedDict


class ScoresDTO(TypedDict):
    CORREL: float
    CHISQR: float
    INTERSECT: float
    BHATTACHARYYA: float


class ImageComparerConverter(Protocol):
    @abstractmethod
    def compare_by_histograms(self, first_image: bytes, second_image: bytes) -> ScoresDTO:
        ...
