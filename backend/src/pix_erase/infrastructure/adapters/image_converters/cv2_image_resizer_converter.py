from typing import override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_resizer import ImageResizerConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageResizerConverter(ImageResizerConverter):
    @override
    def resize(self, data: bytes, image_width: int, image_height: int) -> bytes:
        np_arr: np.ndarray = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        resized_image = cv2.resize(img, (image_width, image_height))
        _, buffer = cv2.imencode(".jpg", resized_image)
        return buffer.tobytes()
