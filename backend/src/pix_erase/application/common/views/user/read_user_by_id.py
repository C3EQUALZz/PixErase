from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadUserByIDView:
    user_id: UUID
    email: str
    name: str
    role: str