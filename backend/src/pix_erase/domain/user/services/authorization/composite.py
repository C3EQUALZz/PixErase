from typing import override, Final

from pix_erase.domain.user.services.authorization.base import (
    Permission,
    PermissionContext,
)


class AnyOf[PC: PermissionContext](Permission[PC]):
    def __init__(self, *permissions: Permission[PC]) -> None:
        self._permissions: Final[tuple[Permission[PC], ...]] = permissions

    @override
    def is_satisfied_by(self, context: PC) -> bool:
        return any(p.is_satisfied_by(context) for p in self._permissions)
