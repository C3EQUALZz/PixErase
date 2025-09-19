from dataclasses import dataclass

from pix_erase.domain.common.entities.base_aggregate import BaseAggregateRoot
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize


@dataclass(eq=False)
class Image(BaseAggregateRoot[ImageID]):
    data: bytes
    width: ImageSize
    height: ImageSize
    name: ImageName
