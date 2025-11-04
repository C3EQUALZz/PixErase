from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime

from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize


@dataclass(frozen=True, slots=True, kw_only=True)
class ImageStreamQueryModel:
    """DTO для стриминга изображения"""

    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: int
    width: ImageSize
    height: ImageSize
    filename: ImageName
    etag: str | None = None
    created_at: datetime
    updated_at: datetime
