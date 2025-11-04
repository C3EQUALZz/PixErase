from typing import override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_comparer_converter import ImageComparerConverter, ScoresDTO
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


def _calculate_ssim(img1: cv2.typing.MatLike, img2: cv2.typing.MatLike) -> float:
    """
    Calculate Structural Similarity Index (SSIM) between two images.
    SSIM measures the structural similarity between two images.
    Returns a value between -1 and 1, where 1 means identical images.
    """
    # Convert to grayscale if needed
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1

    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2

    # Resize images to same size if needed
    if img1_gray.shape != img2_gray.shape:
        img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))

    # Constants for SSIM calculation
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # Calculate means
    mu1 = cv2.GaussianBlur(img1_gray.astype(np.float64), (11, 11), 1.5)
    mu2 = cv2.GaussianBlur(img2_gray.astype(np.float64), (11, 11), 1.5)

    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2

    # Calculate variances and covariance
    sigma1_sq = cv2.GaussianBlur((img1_gray.astype(np.float64) - mu1) ** 2, (11, 11), 1.5)
    sigma2_sq = cv2.GaussianBlur((img2_gray.astype(np.float64) - mu2) ** 2, (11, 11), 1.5)
    sigma12 = cv2.GaussianBlur(
        (img1_gray.astype(np.float64) - mu1) * (img2_gray.astype(np.float64) - mu2), (11, 11), 1.5
    )

    # Calculate SSIM
    ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))
    return float(np.mean(ssim_map))  # type: ignore[arg-type]


def _calculate_mse(img1: cv2.typing.MatLike, img2: cv2.typing.MatLike) -> float:
    """
    Calculate Mean Squared Error (MSE) between two images.
    Lower values indicate more similar images.
    """
    # Resize images to same size if needed
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Convert to same type and calculate MSE
    img1_float = img1.astype(np.float64)
    img2_float = img2.astype(np.float64)

    mse = np.mean((img1_float - img2_float) ** 2)
    return float(mse)


def _calculate_psnr(img1: cv2.typing.MatLike, img2: cv2.typing.MatLike) -> float:
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR) between two images.
    Higher values indicate more similar images.
    Returns infinity if images are identical (MSE = 0).
    """
    mse = _calculate_mse(img1, img2)
    if mse == 0:
        return float("inf")

    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return float(psnr)


class Cv2ImageComparerConverter(ImageComparerConverter):
    @override
    def compare_by_histograms(self, first_image: bytes, second_image: bytes) -> ScoresDTO:
        cv2_first_image: cv2.typing.MatLike | None = cv2.imdecode(
            np.frombuffer(first_image, dtype=np.uint8), cv2.IMREAD_COLOR
        )

        if cv2_first_image is None:
            msg = "Failed to decoding first image"
            raise ImageDecodingError(msg)

        cv2_second_image: cv2.typing.MatLike | None = cv2.imdecode(
            np.frombuffer(second_image, dtype=np.uint8), cv2.IMREAD_COLOR
        )

        if cv2_second_image is None:
            msg = "Failed to decoding second image"
            raise ImageDecodingError(msg)

        # Convert to grayscale for histogram comparison
        gray1 = cv2.cvtColor(cv2_first_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(cv2_second_image, cv2.COLOR_BGR2GRAY)

        # Calculate histograms
        hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

        # Normalize histograms
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Compare histograms
        methods_and_scores: ScoresDTO = {
            "CORREL": 0.0,
            "CHISQR": 0.0,
            "INTERSECT": 0.0,
            "BHATTACHARYYA": 0.0,
            "MSE": 0.0,
            "PSNR": 0.0,
            "SSIM": 0.0,
        }

        # Calculate histogram comparison methods
        for method in ["CORREL", "CHISQR", "INTERSECT", "BHATTACHARYYA"]:
            score = cv2.compareHist(hist1, hist2, getattr(cv2, f"HISTCMP_{method}"))
            methods_and_scores[method] = score  # type: ignore[literal-required]

        # Calculate additional metrics
        methods_and_scores["MSE"] = _calculate_mse(cv2_first_image, cv2_second_image)
        methods_and_scores["PSNR"] = _calculate_psnr(cv2_first_image, cv2_second_image)
        methods_and_scores["SSIM"] = _calculate_ssim(cv2_first_image, cv2_second_image)

        return methods_and_scores
