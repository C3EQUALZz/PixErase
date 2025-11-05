import pytest

from pix_erase.domain.user.services.authorization.permission import (
    CanManageRole,
    CanManageSelf,
    CanManageSubordinate,
    RoleManagementContext,
    UserManagementContext,
)
from pix_erase.domain.user.values.user_role import UserRole
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


def test_can_manage_self_returns_true_when_subject_equals_target() -> None:
    # Arrange
    same_user = create_user(user_id=create_user_id())
    context = UserManagementContext(subject=same_user, target=same_user)
    sut = CanManageSelf()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is True


def test_can_manage_self_returns_false_when_subject_differs_from_target() -> None:
    # Arrange
    subject = create_user(user_id=create_user_id())
    target = create_user(user_id=create_user_id())
    context = UserManagementContext(subject=subject, target=target)
    sut = CanManageSelf()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is False


@pytest.mark.parametrize(
    ("subject_role", "target_role", "expected"),
    [
        pytest.param(UserRole.SUPER_ADMIN, UserRole.ADMIN, True, id="super_admin_can_manage_admin"),
        pytest.param(UserRole.SUPER_ADMIN, UserRole.USER, True, id="super_admin_can_manage_user"),
        pytest.param(UserRole.ADMIN, UserRole.USER, True, id="admin_can_manage_user"),
        pytest.param(UserRole.ADMIN, UserRole.ADMIN, False, id="admin_cannot_manage_admin"),
        pytest.param(UserRole.ADMIN, UserRole.SUPER_ADMIN, False, id="admin_cannot_manage_super_admin"),
        pytest.param(UserRole.USER, UserRole.USER, False, id="user_cannot_manage_user"),
        pytest.param(UserRole.USER, UserRole.ADMIN, False, id="user_cannot_manage_admin"),
    ],
)
def test_can_manage_subordinate_checks_role_hierarchy(
    subject_role: UserRole,
    target_role: UserRole,
    expected: bool,
) -> None:
    # Arrange
    subject = create_user(role=subject_role)
    target = create_user(role=target_role)
    context = UserManagementContext(subject=subject, target=target)
    sut = CanManageSubordinate()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is expected


def test_can_manage_subordinate_returns_false_when_subject_has_no_subordinates() -> None:
    # Arrange
    subject = create_user(role=UserRole.USER)
    target = create_user(role=UserRole.USER)
    context = UserManagementContext(subject=subject, target=target)
    sut = CanManageSubordinate()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is False


@pytest.mark.parametrize(
    ("subject_role", "target_role", "expected"),
    [
        pytest.param(UserRole.SUPER_ADMIN, UserRole.ADMIN, True, id="super_admin_can_assign_admin"),
        pytest.param(UserRole.SUPER_ADMIN, UserRole.USER, True, id="super_admin_can_assign_user"),
        pytest.param(UserRole.ADMIN, UserRole.USER, True, id="admin_can_assign_user"),
        pytest.param(UserRole.ADMIN, UserRole.ADMIN, False, id="admin_cannot_assign_admin"),
        pytest.param(UserRole.ADMIN, UserRole.SUPER_ADMIN, False, id="admin_cannot_assign_super_admin"),
        pytest.param(UserRole.USER, UserRole.USER, False, id="user_cannot_assign_user"),
        pytest.param(UserRole.USER, UserRole.ADMIN, False, id="user_cannot_assign_admin"),
        pytest.param(UserRole.SUPER_ADMIN, UserRole.SUPER_ADMIN, False, id="super_admin_cannot_assign_super_admin"),
    ],
)
def test_can_manage_role_checks_role_hierarchy(
    subject_role: UserRole,
    target_role: UserRole,
    expected: bool,
) -> None:
    # Arrange
    subject = create_user(role=subject_role)
    context = RoleManagementContext(subject=subject, target_role=target_role)
    sut = CanManageRole()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is expected


def test_can_manage_role_returns_false_when_subject_cannot_assign_role() -> None:
    # Arrange
    subject = create_user(role=UserRole.USER)
    context = RoleManagementContext(subject=subject, target_role=UserRole.ADMIN)
    sut = CanManageRole()

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is False
