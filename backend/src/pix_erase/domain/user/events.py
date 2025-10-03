from dataclasses import dataclass
from uuid import UUID

from pix_erase.domain.common.events import BaseDomainEvent


@dataclass(frozen=True, slots=True, eq=False)
class UserCreatedEvent(BaseDomainEvent):
    user_id: UUID
    email: str
    name: str
    role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedPasswordEvent(BaseDomainEvent):
    user_id: UUID
    name: str
    email: str
    role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedNameEvent(BaseDomainEvent):
    user_id: UUID
    old_name: str
    new_name: str
    email: str
    role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedEmailEvent(BaseDomainEvent):
    user_id: UUID
    name: str
    old_email: str
    new_email: str
    role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserDeletedEvent(BaseDomainEvent):
    user_id: UUID


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedRoleEvent(BaseDomainEvent):
    user_id: UUID
    old_role: str
    new_role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserToggleActivationEvent(BaseDomainEvent):
    user_id: UUID
    is_active: bool


@dataclass(frozen=True, slots=True, eq=False)
class UserAddedPhotoEvent(BaseDomainEvent):
    user_id: UUID
    photo_id: UUID
