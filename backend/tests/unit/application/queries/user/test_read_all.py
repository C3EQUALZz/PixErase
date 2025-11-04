from unittest.mock import Mock

import pytest

from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.queries.users.read_all import (
    ReadAllUsersQuery,
    ReadAllUsersQueryHandler,
)
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id, create_username


@pytest.mark.parametrize(
    ("limit", "offset", "sorting_field", "sorting_order"),
    [
        (10, 0, "name", SortingOrder.ASC),
        (20, 5, "email", SortingOrder.DESC),
    ],
)
async def test_read_all_users_success(
    limit: int,
    offset: int,
    sorting_field: str,
    sorting_order: SortingOrder,
    fake_user_query_gateway: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test successful reading all users."""
    users = [create_user(user_id=create_user_id(), username=create_username(f"User{i}")) for i in range(3)]
    fake_user_query_gateway.read_all_users.return_value = users

    handler = ReadAllUsersQueryHandler(
        fake_user_query_gateway,
        fake_current_user_service,
        fake_access_service,
    )

    query = ReadAllUsersQuery(limit=limit, offset=offset, sorting_field=sorting_field, sorting_order=sorting_order)
    result = await handler(query)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_query_gateway.read_all_users.assert_called_once()
    assert len(result) == 3
    assert all(user.id in {u.id for u in result} for user in users)


async def test_read_all_users_invalid_sorting(
    fake_user_query_gateway: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test reading all users fails with invalid sorting field."""
    fake_user_query_gateway.read_all_users.return_value = None

    handler = ReadAllUsersQueryHandler(
        fake_user_query_gateway,
        fake_current_user_service,
        fake_access_service,
    )

    query = ReadAllUsersQuery(limit=10, offset=0, sorting_field="invalid_field", sorting_order=SortingOrder.ASC)
    with pytest.raises(ValueError):  # noqa: PT011
        await handler(query)

    fake_current_user_service.get_current_user.assert_called_once()


async def test_read_all_users_empty_result(
    fake_user_query_gateway: Mock,
    fake_current_user_service: Mock,
    fake_access_service: Mock,
) -> None:
    """Test reading all users returns empty list."""
    fake_user_query_gateway.read_all_users.return_value = []

    handler = ReadAllUsersQueryHandler(
        fake_user_query_gateway,
        fake_current_user_service,
        fake_access_service,
    )

    query = ReadAllUsersQuery(limit=10, offset=0, sorting_field="name", sorting_order=SortingOrder.ASC)
    result = await handler(query)

    fake_current_user_service.get_current_user.assert_called_once()
    fake_user_query_gateway.read_all_users.assert_called_once()
    assert len(result) == 0
