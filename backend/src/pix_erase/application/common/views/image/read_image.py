from dataclasses import dataclass
from datetime import datetime
from typing import AsyncGenerator


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadImageByIDView:
    data: AsyncGenerator[bytes, None]
    name: str
    height: int
    width: int
    content_type: str
    content_length: int
    etag: str | None
    created_at: datetime
    updated_at: datetime
