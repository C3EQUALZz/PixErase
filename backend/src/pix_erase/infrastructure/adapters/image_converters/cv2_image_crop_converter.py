import cv2
import numpy as np
from typing_extensions import override

from pix_erase.domain.image.ports.image_crop_converter import ImageCropConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageCropConverter(ImageCropConverter):
    @override
    def convert(self, data: bytes, new_width: int, new_height: int) -> bytes:
        # Преобразуем байты в массив NumPy
        buffer: np.ndarray = np.frombuffer(data, np.uint8)

        # Декодируем изображение
        img: cv2.typing.MatLike | None = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

        if img is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        # Изменяем размер изображения
        resized_img: cv2.typing.MatLike = cv2.resize(img, (new_width, new_height))

        # Кодируем изображение обратно в байты
        _, buffer = cv2.imencode('.jpg', resized_img)

        return buffer.tobytes()
