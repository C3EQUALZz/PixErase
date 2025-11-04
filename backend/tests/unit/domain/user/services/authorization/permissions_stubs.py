from pix_erase.domain.user.services.authorization.base import (
    Permission,
    PermissionContext,
)


class DummyContext(PermissionContext):
    pass


class AlwaysAllow(Permission[DummyContext]):
    def is_satisfied_by(self, context: DummyContext) -> bool:  # noqa: ARG002
        return True


class AlwaysDeny(Permission[DummyContext]):
    def is_satisfied_by(self, context: DummyContext) -> bool:  # noqa: ARG002
        return False
