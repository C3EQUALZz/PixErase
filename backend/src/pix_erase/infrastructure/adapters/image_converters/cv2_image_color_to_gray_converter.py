import cv2
import numpy as np
from typing_extensions import override

from pix_erase.domain.image.ports.image_color_to_gray_converter import ImageColorToCrayScaleConverter
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError


class Cv2ImageColorToCrayScaleConverter(ImageColorToCrayScaleConverter):
    @override
    def convert(self, data: bytes) -> bytes:
        cv2_image: cv2.typing.MatLike | None = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

        if cv2_image is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        gray_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

        _, encoded_img = cv2.imencode(".jpg", gray_image)

        return encoded_img.tobytes()
