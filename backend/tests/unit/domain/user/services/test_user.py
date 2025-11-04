from unittest.mock import Mock

import pytest

from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.errors.user import (
    RoleAssignmentNotPermittedError,
)
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.user_role import UserRole
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import (
    create_password_hash,
    create_raw_password,
    create_user_email,
    create_user_id,
    create_username,
)


@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)
def test_creates_active_user_with_hashed_password(
    role: UserRole,
    user_id_generator: Mock,
    password_hasher: Mock,
) -> None:
    # Arrange
    email = create_user_email()
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()

    user_id_generator.return_value = expected_id
    password_hasher.hash.return_value = expected_hash
    sut = UserService(password_hash_service=password_hasher, user_id_generator=user_id_generator)

    # Act
    result = sut.create(email=email, name=username, raw_password=raw_password, role=role)

    # Assert
    assert isinstance(result, User)
    assert result.id == expected_id
    assert result.email == email
    assert result.name == username
    assert result.hashed_password == expected_hash
    assert result.role == role
    assert result.is_active is True


def test_fails_to_create_user_with_unassignable_role(
    user_id_generator: Mock,
    password_hasher: Mock,
) -> None:
    email = create_user_email()
    username = create_username()
    raw_password = create_raw_password()
    sut = UserService(password_hash_service=password_hasher, user_id_generator=user_id_generator)

    with pytest.raises(RoleAssignmentNotPermittedError):
        sut.create(
            email=email,
            name=username,
            raw_password=raw_password,
            role=UserRole.SUPER_ADMIN,
        )


@pytest.mark.parametrize(
    "is_valid",
    [True, False],
)
def test_checks_password_authenticity(
    is_valid: bool,
    user_id_generator: Mock,
    password_hasher: Mock,
) -> None:
    # Arrange
    user = create_user()
    raw_password = create_raw_password()

    password_hasher.verify.return_value = is_valid
    sut = UserService(password_hash_service=password_hasher, user_id_generator=user_id_generator)

    # Act
    result = sut.is_password_valid(user, raw_password)

    # Assert
    assert result is is_valid


def test_changes_password(
    user_id_generator: Mock,
    password_hasher: Mock,
) -> None:
    # Arrange
    initial_hash = create_password_hash(b"old")
    user = create_user(password_hash=initial_hash)
    raw_password = create_raw_password()

    expected_hash = create_password_hash(b"new")
    password_hasher.hash.return_value = expected_hash
    sut = UserService(password_hash_service=password_hasher, user_id_generator=user_id_generator)

    # Act
    sut.change_password(user, raw_password)

    # Assert
    assert user.hashed_password == expected_hash
