from dataclasses import dataclass

from pix_erase.domain.common.events import BaseDomainEvent


@dataclass(frozen=True, slots=True, eq=False)
class ImageConvertedEvent(BaseDomainEvent):
    name: str
    width: int
    height: int
    method: str
