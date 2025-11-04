from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.change_user_name import (
    ChangeUserNameByIDCommand,
    ChangeUserNameByIDCommandHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.values.user_id import UserID
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id, create_username


@pytest.mark.parametrize(
    ("user_id", "new_name"),
    [
        (create_user_id(), "New_Name_1"),
        (create_user_id(), "New_Name_2"),
    ],
)
async def test_change_user_name_success(
    user_id: UserID,
    new_name: str,
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful username change."""
    target_user = create_user(user_id=user_id)
    fake_user_command_gateway.read_by_id.return_value = target_user

    handler = ChangeUserNameByIDCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
    )

    command = ChangeUserNameByIDCommand(user_id=user_id, new_name=new_name)
    await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_name.assert_called_once_with(user=target_user, new_user_name=create_username(new_name))
    fake_event_bus.publish.assert_called_once()
    fake_transaction.commit.assert_called_once()


async def test_change_user_name_not_found(
    fake_transaction: Mock,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_event_bus: Mock,
    fake_access_service: Mock,
) -> None:
    """Test name change fails when user not found."""
    user_id = create_user_id()
    fake_user_command_gateway.read_by_id.return_value = None

    handler = ChangeUserNameByIDCommandHandler(
        fake_transaction,
        fake_user_command_gateway,
        fake_user_service,
        fake_current_user_service,
        fake_event_bus,
        fake_access_service,
    )

    command = ChangeUserNameByIDCommand(user_id=user_id, new_name="NewName")
    with pytest.raises(UserNotFoundByIDError, match="Can't find user by ID"):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_user_service.change_name.assert_not_called()
    fake_event_bus.publish.assert_not_called()
    fake_transaction.commit.assert_not_called()
