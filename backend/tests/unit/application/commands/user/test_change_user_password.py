from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.change_user_password import (
    ChangeUserPasswordCommand,
    ChangeUserPasswordCommandHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.values.user_id import UserID
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_raw_password, create_user_id


@pytest.mark.parametrize(
    ("user_id", "password"),
    [
        (create_user_id(), "new_password_1"),
        (create_user_id(), "new_password_2"),
    ],
)
async def test_change_user_password_success(
    user_id: UserID,
    password: str,
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
    fake_auth_session_service: Mock,
) -> None:
    """Test successful user password change."""
    target_user = create_user(user_id=user_id)
    fake_user_command_gateway.read_by_id.return_value = target_user

    handler = ChangeUserPasswordCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
        fake_auth_session_service,
    )

    command = ChangeUserPasswordCommand(user_id=user_id, password=password)
    await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_password.assert_called_once_with(
        user=target_user, raw_password=create_raw_password(password)
    )
    fake_event_bus.publish.assert_called_once()
    fake_transaction.commit.assert_called_once()
    fake_auth_session_service.invalidate_current_session.assert_called_once()


async def test_change_user_password_not_found(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
    fake_auth_session_service: Mock,
) -> None:
    """Test password change fails when user not found."""
    user_id = create_user_id()
    fake_user_command_gateway.read_by_id.return_value = None

    handler = ChangeUserPasswordCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
        fake_auth_session_service,
    )

    command = ChangeUserPasswordCommand(user_id=user_id, password="new_password")
    with pytest.raises(UserNotFoundByIDError, match="Can't find user by ID"):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_password.assert_not_called()
    fake_event_bus.publish.assert_not_called()
    fake_transaction.commit.assert_not_called()
    fake_auth_session_service.invalidate_current_session.assert_not_called()
