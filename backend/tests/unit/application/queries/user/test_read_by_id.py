from unittest.mock import Mock

import pytest

from pix_erase.application.queries.users.read_by_id import (
    ReadUserByIDQuery,
    ReadUserByIDQueryHandler,
)
from pix_erase.application.errors.user import UserNotFoundByIDError

from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


@pytest.mark.parametrize(
    "user_id",
    [
        create_user_id(),
        create_user_id(),
    ],
)
async def test_read_user_by_id_success(
    user_id,
    fake_user_query_gateway: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful reading user by ID."""
    target_user = create_user(user_id=user_id)
    fake_user_query_gateway.read_user_by_id.return_value = target_user

    handler = ReadUserByIDQueryHandler(
        fake_current_user_service,
        fake_user_query_gateway,
        fake_access_service,
    )

    query = ReadUserByIDQuery(user_id=user_id)
    result = await handler(query)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_query_gateway.read_user_by_id.assert_called_once()
    fake_access_service.authorize.assert_called_once()
    assert result.id == target_user.id
    assert result.email == str(target_user.email)
    assert result.name == str(target_user.name)
    assert result.role == target_user.role


async def test_read_user_by_id_not_found(
    fake_user_query_gateway: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test reading user by ID fails when user not found."""
    user_id = create_user_id()
    fake_user_query_gateway.read_user_by_id.return_value = None

    handler = ReadUserByIDQueryHandler(
        fake_current_user_service,
        fake_user_query_gateway,
        fake_access_service,
    )

    query = ReadUserByIDQuery(user_id=user_id)
    with pytest.raises(UserNotFoundByIDError, match="Can't find user by id"):
        await handler(query)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_query_gateway.read_user_by_id.assert_called_once()
    fake_access_service.authorize.assert_not_called()

