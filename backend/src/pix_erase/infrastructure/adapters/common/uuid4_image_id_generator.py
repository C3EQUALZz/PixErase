import uuid
from typing import cast, override

from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.values.image_id import ImageID


class UUID4ImageIdGenerator(ImageIdGenerator):
    @override
    def __call__(self) -> ImageID:
        return cast("ImageID", uuid.uuid4())
