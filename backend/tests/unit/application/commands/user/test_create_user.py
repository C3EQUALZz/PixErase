from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.create_user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from pix_erase.application.errors.user import UserAlreadyExistsError
from pix_erase.domain.user.values.user_role import UserRole

from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import (
    create_user_email,
    create_user_id,
    create_username,
)


@pytest.mark.parametrize(
    ("email", "name", "password", "role"),
    [
        ("user1@example.com", "UserOne", "password123", UserRole.USER),
        ("user2@example.com", "UserTwo", "password456", UserRole.ADMIN),
    ],
)
async def test_create_user_success(
    email: str,
    name: str,
    password: str,
    role: UserRole,
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful user creation."""
    new_user = create_user(
        user_id=create_user_id(),
        username=create_username(name),
        email=create_user_email(email),
        role=role,
    )
    fake_user_service.create.return_value = new_user
    fake_user_command_gateway.read_by_email.return_value = None

    handler = CreateUserCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_event_bus,
        fake_current_user_service,
        fake_access_service,
    )

    command = CreateUserCommand(email=email, name=name, password=password, role=role)
    result = await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_service.create.assert_called_once()
    fake_user_command_gateway.add.assert_called_once_with(new_user)
    fake_transaction.flush.assert_called_once()
    fake_event_bus.publish.assert_called_once()
    fake_transaction.commit.assert_called_once()
    assert result.user_id == new_user.id


async def test_create_user_already_exists(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test user creation fails when user already exists."""
    email = "existing@example.com"
    new_user = create_user(
        user_id=create_user_id(),
        email=create_user_email(email),
    )
    fake_user_service.create.return_value = new_user
    fake_user_command_gateway.read_by_email.return_value = new_user

    handler = CreateUserCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_event_bus,
        fake_current_user_service,
        fake_access_service,
    )

    command = CreateUserCommand(
        email=email,
        name="UserName",
        password="password",
        role=UserRole.USER,
    )
    with pytest.raises(UserAlreadyExistsError):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_service.create.assert_called_once()
    fake_user_command_gateway.add.assert_not_called()
    fake_transaction.flush.assert_not_called()
    fake_event_bus.publish.assert_not_called()
    fake_transaction.commit.assert_not_called()

