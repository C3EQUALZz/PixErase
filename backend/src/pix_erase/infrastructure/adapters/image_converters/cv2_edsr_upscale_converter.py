import logging
from typing import Final

import cv2
import numpy as np
from pathlib import Path
from cv2 import dnn_superres
from typing_extensions import override

from pix_erase.domain.image.ports.image_ai_upscaler_converter import ImageAIUpscaleConverter
from pix_erase.domain.image.values.image_scale import ImageScale
from pix_erase.infrastructure.errors.image_converters import ImageDecodingError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Cv2EDSRImageUpscaleConverter(ImageAIUpscaleConverter):
    def __init__(self) -> None:
        self._model_path: str = str(Path(__file__).parent.resolve() / r"models/EDSR_x2.pb")
        self._model_name: str = "edsr"

    @override
    def convert(self, data: bytes, width: int, height: int, scale: ImageScale) -> bytes:
        cv2_image: cv2.typing.MatLike | None = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

        if cv2_image is None:
            msg = "Failed to decoding image"
            raise ImageDecodingError(msg)

        image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

        sr_model: dnn_superres.DnnSuperResImpl = dnn_superres.DnnSuperResImpl.create()

        sr_model.readModel(self._model_path)
        sr_model.setModel(self._model_name, 2)

        upsampled_image = sr_model.upsample(image)

        _, encoded_img = cv2.imencode(".jpg", upsampled_image)

        return encoded_img.tobytes()
