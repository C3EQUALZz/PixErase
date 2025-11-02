from dataclasses import dataclass

from pix_erase.domain.common.entities.base_entity import BaseEntity
from pix_erase.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, slots=True, repr=False)
class NamedEntityId(BaseValueObject):
    value: int

    def _validate(self) -> None:
        ...

    def __str__(self) -> str:
        return str(self.value)


class NamedEntity(BaseEntity[NamedEntityId]):
    def __init__(self, *, id_: NamedEntityId, name: str) -> None:
        super().__init__(id=id_)
        self.name = name


class NamedEntitySubclass(NamedEntity):
    def __init__(self, *, id_: NamedEntityId, name: str, value: int) -> None:
        super().__init__(id_=id_, name=name)
        self.value = value


def create_named_entity_id(
    id_: int = 42,
) -> NamedEntityId:
    return NamedEntityId(value=id_)


def create_named_entity(
    id_: int = 42,
    name: str = "name",
) -> NamedEntity:
    return NamedEntity(id_=NamedEntityId(id_), name=name)


def create_named_entity_subclass(
    id_: int = 42,
    name: str = "name",
    value: int = 314,
) -> NamedEntitySubclass:
    return NamedEntitySubclass(id_=NamedEntityId(id_), name=name, value=value)