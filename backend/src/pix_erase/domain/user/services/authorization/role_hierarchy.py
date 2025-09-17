from collections.abc import Mapping
from typing import Final

from pix_erase.domain.user.values.user_role import UserRole

SUBORDINATE_ROLES: Final[Mapping[UserRole, set[UserRole]]] = {
    UserRole.SUPER_ADMIN: {UserRole.ADMIN, UserRole.ANNOTATOR},
    UserRole.ADMIN: {UserRole.ANNOTATOR},
    UserRole.ANNOTATOR: set(),
}
