from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.activate_user import (
    ActivateUserCommand,
    ActivateUserCommandHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


async def test_activate_user_success(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful user activation."""
    user_id = create_user_id()
    target_user = create_user(user_id=user_id, is_active=False)
    fake_user_command_gateway.read_by_id.return_value = target_user

    handler = ActivateUserCommandHandler(
        fake_current_user_service,
        fake_user_command_gateway,
        fake_user_service,
        fake_transaction,
        fake_access_service,
    )

    command = ActivateUserCommand(user_id=user_id)
    await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_access_service.toggle_user_activation.assert_called_once_with(target_user, is_active=True)
    fake_transaction.commit.assert_called_once()


async def test_activate_user_not_found(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test activation fails when user not found."""
    user_id = create_user_id()
    fake_user_command_gateway.read_by_id.return_value = None

    handler = ActivateUserCommandHandler(
        fake_current_user_service,
        fake_user_command_gateway,
        fake_user_service,
        fake_transaction,
        fake_access_service,
    )

    command = ActivateUserCommand(user_id=user_id)
    with pytest.raises(UserNotFoundByIDError, match="Can't find user by ID"):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_access_service.toggle_user_activation.assert_not_called()
    fake_transaction.commit.assert_not_called()
