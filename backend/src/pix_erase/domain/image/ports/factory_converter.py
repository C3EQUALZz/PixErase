from abc import abstractmethod
from enum import Enum
from typing import Protocol

from pix_erase.domain.image.ports.converter import ImageConverter


class ImageConverterType(Enum):
    GRAY_TO_COLOR = "gray_to_image"
    COLOR_TO_GRAY = "color_to_image"
    REMOVE_WATERMARK = "remove_watermark"


class FactoryConverter(Protocol):
    @abstractmethod
    def create_image_converter(self, image_converter_type: ImageConverterType) -> ImageConverter: ...
