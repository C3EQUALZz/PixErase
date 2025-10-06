from tempfile import TemporaryFile

import torch
from PIL import Image
from super_image import EdsrModel, ImageLoader
from torch import Tensor
from typing_extensions import override

from pix_erase.domain.image.ports.image_upscaler_converter import ImageUpscaleConverter


def upscaler_model_provider() -> EdsrModel:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model: EdsrModel = EdsrModel.from_pretrained(
        'eugenesiow/edsr-base',
        scale=2
    )
    model.to(device)
    return model


class SuperImageUpscalerConverter(ImageUpscaleConverter):
    def __init__(self, model: EdsrModel) -> None:
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model: EdsrModel = model.to(self._device)

    @override
    def convert(self, data: bytes, width: int, height: int) -> bytes:
        tensor: Tensor = ImageLoader.load_image(Image.frombytes(mode="RGB", data=data, size=(width, height)))

        with TemporaryFile() as temp:
            ImageLoader.save_image(pred=self._model(tensor.to(self._device)), output_file=temp.name)
            return temp.read()
