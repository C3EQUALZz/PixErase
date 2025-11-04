from typing import override

import cv2
import numpy as np
from rembg import remove

from pix_erase.domain.image.ports.image_background_remove_converter import ImageRemoveBackgroundConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class RembgImageRemoveBackgroundConverter(ImageRemoveBackgroundConverter):
    @override
    def convert(self, data: bytes) -> bytes:
        img_bgr = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        if img_bgr is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        # Конвертируем в RGB для работы
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        cleared_from_background_image = remove(data=img_rgb)
        _, buffer = cv2.imencode(".jpg", cleared_from_background_image)

        return buffer.tobytes()
