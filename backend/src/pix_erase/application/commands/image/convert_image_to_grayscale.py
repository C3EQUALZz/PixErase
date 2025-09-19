from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, slots=True, kw_only=True)
class ConvertImageToGrayscaleCommand:
    data: bytes
    image_name: str


@final
class ConvertImageToGrayscaleCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: ConvertImageToGrayscaleCommand):
        ...
