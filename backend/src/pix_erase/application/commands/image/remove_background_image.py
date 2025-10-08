from dataclasses import dataclass
from typing import final
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RemoveBackgroundImageCommand:
    image_id: UUID


@final
class RemoveBackgroundImageCommandHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Changes existing image.
    """
    def __init__(self) -> None:
        ...

    async def __call__(self, data: RemoveBackgroundImageCommand):
        ...
