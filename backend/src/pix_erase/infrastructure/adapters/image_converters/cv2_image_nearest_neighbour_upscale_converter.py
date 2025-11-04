import math
from typing import override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_nearest_neighbour_upscale_converter import (
    ImageNearestNeighbourUpscalerConverter,
)
from pix_erase.domain.image.values.image_scale import ImageScale
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageNearestNeighbourUpscalerConverter(ImageNearestNeighbourUpscalerConverter):
    @override
    def convert(self, data: bytes, width: int, height: int, scale: ImageScale) -> bytes:
        np_arr: np.ndarray = np.frombuffer(data, np.uint8)
        # Декодируем изображение
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        resized_height: int = height * scale.value
        resized_width: int = width * scale.value
        resized: np.ndarray = np.zeros((resized_height, resized_width, 3), np.uint8)

        ratio_for_col: float = height / resized_height
        ratio_for_row: float = width / resized_width

        for x in range(resized_width):
            for y in range(resized_height):
                resized[y, x] = img[math.ceil((y + 1) * ratio_for_col) - 1, math.ceil((x + 1) * ratio_for_row) - 1]

        _, encoded_img = cv2.imencode(".jpg", resized)

        return encoded_img.tobytes()
