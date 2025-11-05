from pix_erase.domain.user.services.authorization.composite import AnyOf
from pix_erase.domain.user.services.authorization.permission import (
    CanManageSelf,
    CanManageSubordinate,
    UserManagementContext,
)
from pix_erase.domain.user.values.user_role import UserRole
from tests.unit.domain.user.services.authorization.permissions_stubs import AlwaysAllow, AlwaysDeny, DummyContext
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


def test_any_of_returns_true_when_first_permission_satisfied() -> None:
    # Arrange
    same_user = create_user(user_id=create_user_id())
    context = UserManagementContext(subject=same_user, target=same_user)
    sut = AnyOf(CanManageSelf(), CanManageSubordinate())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is True


def test_any_of_returns_true_when_second_permission_satisfied() -> None:
    # Arrange
    super_admin = create_user(role=UserRole.SUPER_ADMIN)
    user = create_user(role=UserRole.USER)
    context = UserManagementContext(subject=super_admin, target=user)
    sut = AnyOf(CanManageSelf(), CanManageSubordinate())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is True


def test_any_of_returns_true_when_both_permissions_satisfied() -> None:
    # Arrange
    same_user = create_user(user_id=create_user_id(), role=UserRole.SUPER_ADMIN)
    context = UserManagementContext(subject=same_user, target=same_user)
    sut = AnyOf(CanManageSelf(), CanManageSubordinate())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is True


def test_any_of_returns_false_when_no_permission_satisfied() -> None:
    # Arrange
    user1 = create_user(user_id=create_user_id(), role=UserRole.USER)
    user2 = create_user(user_id=create_user_id(), role=UserRole.USER)
    context = UserManagementContext(subject=user1, target=user2)
    sut = AnyOf(CanManageSelf(), CanManageSubordinate())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is False


def test_any_of_with_single_permission() -> None:
    # Arrange
    same_user = create_user(user_id=create_user_id())
    context = UserManagementContext(subject=same_user, target=same_user)
    sut = AnyOf(CanManageSelf())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is True


def test_any_of_with_single_permission_returns_false() -> None:
    # Arrange
    user1 = create_user(user_id=create_user_id())
    user2 = create_user(user_id=create_user_id())
    context = UserManagementContext(subject=user1, target=user2)
    sut = AnyOf(CanManageSelf())

    # Act
    result = sut.is_satisfied_by(context)

    # Assert
    assert result is False


def test_any_of_allows_if_at_least_one_allows() -> None:
    sut = AnyOf(AlwaysDeny(), AlwaysAllow())
    assert sut.is_satisfied_by(DummyContext())


def test_any_of_denies_if_all_deny() -> None:
    sut = AnyOf(AlwaysDeny(), AlwaysDeny())
    assert not sut.is_satisfied_by(DummyContext())


def test_any_of_empty_returns_false() -> None:
    sut: AnyOf[DummyContext] = AnyOf()
    assert not sut.is_satisfied_by(DummyContext())
