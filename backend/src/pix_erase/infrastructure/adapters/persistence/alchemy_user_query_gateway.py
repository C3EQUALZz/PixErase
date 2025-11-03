import logging
from collections.abc import Sequence
from typing import override, Final
from uuid import UUID

from sqlalchemy import ColumnElement, Select, Result, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserListParams
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_role import UserRole
from pix_erase.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from pix_erase.infrastructure.errors.transaction_manager import RepoError
from pix_erase.infrastructure.persistence.models.users import users_table

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SqlAlchemyUserQueryGateway(UserQueryGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        table_sorting_field: ColumnElement[UUID | str | UserRole | bool] | None = ( # type: ignore[unused-ignore]
            users_table.c.get(user_list_params.sorting.sorting_field)
        )
        if table_sorting_field is None:
            logger.error(
                "Invalid sorting field: '%s'.",
                user_list_params.sorting.sorting_field,
            )
            return None

        order_by: ColumnElement[UUID | str | UserRole | bool] = (
            table_sorting_field.asc()
            if user_list_params.sorting.sorting_order == SortingOrder.ASC
            else table_sorting_field.desc()
        )

        select_stmt: Select[tuple[User]] = (
            select(
                User
            )
            .order_by(order_by)
            .limit(user_list_params.pagination.limit)
            .offset(user_list_params.pagination.offset)
        )

        try:
            result: Result[
                tuple[User]
            ] = await self._session.execute(select_stmt)
            rows: Sequence[User] = result.scalars().fetchall()

            return list(rows)

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
