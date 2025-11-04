import pytest

from pix_erase.domain.user.errors.access_service import AuthorizationError
from pix_erase.domain.user.services.access_service import AccessService
from tests.unit.domain.user.services.authorization.permissions_stubs import AlwaysAllow, AlwaysDeny, DummyContext


def test_authorize_allows_when_permission_is_satisfied() -> None:
    context = DummyContext()
    permission = AlwaysAllow()
    access_service = AccessService()

    access_service.authorize(permission, context=context)


def test_authorize_raises_when_permission_not_satisfied() -> None:
    context = DummyContext()
    permission = AlwaysDeny()
    access_service = AccessService()

    with pytest.raises(AuthorizationError):
        access_service.authorize(permission, context=context)
