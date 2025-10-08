import logging
from typing import Final, override

import cv2
import numpy as np

from pix_erase.domain.image.ports.image_watermark_remover_converter import ImageWatermarkRemoverConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError

logger: Final[logging.Logger] = logging.getLogger(__name__)


def create_adaptive_mask(img_rgb: np.ndarray) -> np.ndarray:
    """Адаптивное создание маски с использованием нескольких методов"""
    # Метод 1: Порог по яркости
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    _, mask_brightness = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Метод 2: HSV для темных цветов
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    mask_dark = (hsv[:, :, 2] < 150).astype(np.uint8) * 255

    # Комбинируем маски
    combined_mask = cv2.bitwise_or(mask_brightness, mask_dark)

    return combined_mask


class Cv2ImageWatermarkRemover(ImageWatermarkRemoverConverter):
    @override
    def convert(self, data: bytes) -> bytes:
        img_bgr = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        if img_bgr is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        # Конвертируем в RGB для работы
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # Создаем маску текста (адаптивно)
        text_mask = create_adaptive_mask(img_rgb)

        # Улучшаем маску морфологическими операциями
        kernel = np.ones((2, 2), np.uint8)
        text_mask = cv2.morphologyEx(text_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
        text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel)

        # Инпантинг вместо простой заливки
        result = cv2.inpaint(img_bgr, text_mask, 3, cv2.INPAINT_TELEA)

        # Кодируем обратно
        success, encoded = cv2.imencode('.jpg', result)
        return encoded.tobytes() if success else data
