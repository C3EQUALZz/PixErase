import cv2
import numpy as np
from typing_extensions import override

from pix_erase.domain.image.ports.image_compress_converter import ImageCompressConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageCompressConverter(ImageCompressConverter):
    @override
    def convert(self, data: bytes, quality: int = 90) -> bytes:
        # Преобразуем байты в массив NumPy
        np_arr: np.ndarray = np.frombuffer(data, np.uint8)
        # Декодируем изображение
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        # Кодируем изображение с заданным качеством
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode('.jpg', img, encode_param)

        return buffer.tobytes()
