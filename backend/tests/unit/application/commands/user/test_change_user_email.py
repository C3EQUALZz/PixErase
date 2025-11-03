from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.change_user_email import (
    ChangeUserEmailCommand,
    ChangeUserEmailCommandHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.values.user_id import UserID

from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_email, create_user_id


@pytest.mark.parametrize(
    ("user_id", "new_email"),
    [
        (create_user_id(), "new_email1@example.com"),
        (create_user_id(), "new_email2@example.com"),
    ],
)
async def test_change_user_email_success(
    user_id: UserID,
    new_email: str,
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful user email change."""
    target_user = create_user(user_id=user_id)
    fake_user_command_gateway.read_by_id.return_value = target_user

    handler = ChangeUserEmailCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
    )

    command = ChangeUserEmailCommand(user_id=user_id, new_email=new_email)
    await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_email.assert_called_once_with(
        target_user, create_user_email(new_email)
    )
    fake_event_bus.publish.assert_called_once()
    fake_transaction.commit.assert_called_once()


async def test_change_user_email_not_found(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test email change fails when user not found."""
    user_id = create_user_id()
    fake_user_command_gateway.read_by_id.return_value = None

    handler = ChangeUserEmailCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
    )

    command = ChangeUserEmailCommand(user_id=user_id, new_email="new@example.com")
    with pytest.raises(UserNotFoundByIDError, match="Cant find user by ID"):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_email.assert_not_called()
    fake_event_bus.publish.assert_not_called()
    fake_transaction.commit.assert_not_called()

