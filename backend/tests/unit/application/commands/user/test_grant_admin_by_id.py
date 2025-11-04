from unittest.mock import Mock

import pytest

from pix_erase.application.commands.user.grant_admin_by_id import (
    GrantAdminToUserByIDCommand,
    GrantAdminToUserByIDCommandHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError
from pix_erase.domain.user.values.user_id import UserID
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


@pytest.mark.parametrize(
    "user_id",
    [create_user_id() for _ in range(3)],
)
async def test_grant_admin_by_id_success(
    user_id: UserID,
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_transaction: Mock,
    fake_access_service: Mock,
    fake_event_bus: Mock,
) -> None:
    """Test successful granting admin role."""
    target_user = create_user(user_id=user_id)
    fake_user_command_gateway.read_by_id.return_value = target_user

    handler = GrantAdminToUserByIDCommandHandler(
        fake_current_user_service,
        fake_user_command_gateway,
        fake_user_service,
        fake_transaction,
        fake_access_service,
        fake_event_bus,
    )

    command = GrantAdminToUserByIDCommand(user_id=user_id)
    await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_access_service.toggle_user_admin_role.assert_called_once_with(target_user, is_admin=True)
    fake_event_bus.publish.assert_called_once()
    fake_transaction.commit.assert_called_once()


async def test_grant_admin_by_id_not_found(
    fake_user_command_gateway: Mock,
    fake_user_service: Mock,
    fake_current_user_service: Mock,
    fake_transaction: Mock,
    fake_access_service: Mock,
    fake_event_bus: Mock,
) -> None:
    """Test grant admin fails when user not found."""
    user_id = create_user_id()
    fake_user_command_gateway.read_by_id.return_value = None

    handler = GrantAdminToUserByIDCommandHandler(
        fake_current_user_service,
        fake_user_command_gateway,
        fake_user_service,
        fake_transaction,
        fake_access_service,
        fake_event_bus,
    )

    command = GrantAdminToUserByIDCommand(user_id=user_id)
    with pytest.raises(UserNotFoundByIDError, match="Can't find user by ID"):
        await handler(command)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_command_gateway.read_by_id.assert_called_once()
    fake_access_service.toggle_user_admin_role.assert_not_called()
    fake_event_bus.publish.assert_not_called()
    fake_transaction.commit.assert_not_called()
