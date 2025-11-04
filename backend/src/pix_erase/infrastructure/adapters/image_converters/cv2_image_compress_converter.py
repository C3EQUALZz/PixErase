from typing import override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_compress_converter import ImageCompressConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageCompressConverter(ImageCompressConverter):
    @override
    def convert(self, data: bytes, quality: int = 90) -> bytes:
        np_arr: np.ndarray = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode(".jpg", img, encode_param)

        return buffer.tobytes()
