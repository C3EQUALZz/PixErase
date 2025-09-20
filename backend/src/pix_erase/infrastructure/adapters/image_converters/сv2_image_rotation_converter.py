from typing import override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_rotation_converter import ImageRotationConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageRotationConverter(ImageRotationConverter):
    @override
    def convert(self, data: bytes, angle: int = 90) -> bytes:
        # Преобразуем байты в массив NumPy
        np_arr: np.ndarray = np.frombuffer(data, np.uint8)

        # Декодируем изображение
        img: cv2.typing.MatLike = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        # Получаем размеры изображения
        (h, w) = img.shape[:2]

        # Находим центр изображения
        center: tuple[int, int] = (w // 2, h // 2)

        # Получаем матрицу поворота
        rotation_matrix: cv2.typing.MatLike = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Поворачиваем изображение
        rotated_img: cv2.typing.MatLike = cv2.warpAffine(img, rotation_matrix, (w, h))

        # Кодируем изображение обратно в байты
        _, buffer = cv2.imencode('.jpg', rotated_img)

        return buffer.tobytes()