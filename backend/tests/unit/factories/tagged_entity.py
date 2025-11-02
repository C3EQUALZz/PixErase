from dataclasses import dataclass

from pix_erase.domain.common.entities.base_entity import BaseEntity
from pix_erase.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, slots=True, repr=False)
class TaggedEntityId(BaseValueObject):
    value: int

    def _validate(self) -> None:
        ...

    def __str__(self) -> str:
        ...


class TaggedEntity(BaseEntity[TaggedEntityId]):
    def __init__(self, *, id_: TaggedEntityId, tag: str) -> None:
        super().__init__(id=id_)
        self.tag = tag


def create_tagged_entity_id(id_: int = 54) -> TaggedEntityId:
    return TaggedEntityId(id_)


def create_tagged_entity(id_: int = 54, tag: str = "tag") -> TaggedEntity:
    return TaggedEntity(id_=TaggedEntityId(id_), tag=tag)
