import cv2
import numpy as np
from typing_extensions import override

from pix_erase.domain.image.ports.image_comparer_converter import ScoresDTO, ImageComparerConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageComparerConverter(ImageComparerConverter):
    @override
    def convert(self, first_image: bytes, second_image: bytes) -> bytes:
        ...

    @override
    def compare_by_histograms(self, first_image: bytes, second_image: bytes) -> ScoresDTO:
        cv2_first_image: cv2.typing.MatLike = cv2.imdecode(
            np.frombuffer(first_image, dtype=np.uint8),
            cv2.IMREAD_COLOR
        )

        if cv2_first_image is None:
            msg = "Failed to decoding first image"
            raise ImageDecodingError(msg)

        cv2_second_image: cv2.typing.MatLike = cv2.imdecode(
            np.frombuffer(second_image, dtype=np.uint8),
            cv2.IMREAD_COLOR
        )

        if cv2_second_image is None:
            msg = "Failed to decoding second image"
            raise ImageDecodingError(msg)

        hist1 = cv2.calcHist([cv2_first_image], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([cv2_second_image], [0], None, [256], [0, 256])

        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Compare histograms
        methods_and_scores: ScoresDTO = {
            "CORREL": 0.0,
            "CHISQR": 0.0,
            "INTERSECT": 0.0,
            "BHATTACHARYYA": 0.0
        }
        for method in methods_and_scores:
            score = cv2.compareHist(hist1, hist2, getattr(cv2, f'HISTCMP_{method}'))
            methods_and_scores[method] = score

        return methods_and_scores
