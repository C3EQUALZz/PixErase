from typing import TypedDict
from uuid import UUID

from pix_erase.domain.user.values.user_role import UserRole


class UserQueryModel(TypedDict):
    id: UUID
    username: str
    role: UserRole
    is_active: bool
