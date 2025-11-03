import pytest

from pix_erase.domain.user.errors.access_service import (
    RoleChangeNotPermittedError,
    ActivationChangeNotPermittedError,
)
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.values.user_role import UserRole
from tests.unit.factories.user_entity import create_user


@pytest.mark.parametrize(
    ("initial_state", "target_state"),
    [
        pytest.param(True, False, id="active_to_inactive"),
        pytest.param(False, True, id="inactive_to_active"),
    ],
)
def test_toggles_activation_state(
        initial_state: bool,
        target_state: bool,
) -> None:
    # Arrange
    user = create_user(is_active=initial_state)
    sut = AccessService()

    # Act
    sut.toggle_user_activation(user, is_active=target_state)

    # Assert
    assert user.is_active is target_state


@pytest.mark.parametrize(
    "is_active",
    [True, False],
)
def test_preserves_super_admin_activation_state(
        is_active: bool,
) -> None:
    # Arrange
    user = create_user(role=UserRole.SUPER_ADMIN, is_active=not is_active)
    sut = AccessService()

    # Act & Assert
    with pytest.raises(ActivationChangeNotPermittedError):
        sut.toggle_user_activation(user, is_active=is_active)

    assert user.is_active is not is_active


@pytest.mark.parametrize(
    ("initial_role", "target_is_admin", "expected_role"),
    [
        pytest.param(UserRole.USER, True, UserRole.ADMIN, id="user_to_admin"),
        pytest.param(UserRole.ADMIN, False, UserRole.USER, id="admin_to_user"),
    ],
)
def test_toggles_role(
        initial_role: UserRole,
        target_is_admin: bool,
        expected_role: UserRole,
) -> None:
    # Arrange
    user = create_user(role=initial_role)
    sut = AccessService()

    # Act
    sut.toggle_user_admin_role(user, is_admin=target_is_admin)

    # Assert
    assert user.role == expected_role


@pytest.mark.parametrize(
    "is_admin",
    [True, False],
)
def test_preserves_super_admin_role(
        is_admin: bool,
) -> None:
    # Arrange
    user = create_user(role=UserRole.SUPER_ADMIN)
    sut = AccessService()

    # Act & Assert
    with pytest.raises(RoleChangeNotPermittedError):
        sut.toggle_user_admin_role(user, is_admin=is_admin)

    assert user.role == UserRole.SUPER_ADMIN


