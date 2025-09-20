import logging
from collections.abc import Sequence
from typing import override, Final
from uuid import UUID

from select import select
from sqlalchemy import ColumnElement, Select, Result, Row
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_models.user import UserQueryModel
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserListParams
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_role import UserRole
from pix_erase.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from pix_erase.infrastructure.errors.transaction_manager import RepoError

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
    async def read_all_users(self, user_list_params: UserListParams) -> list[UserQueryModel] | None:
        table_sorting_field: ColumnElement[UUID | str | UserRole | bool] | None = (
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

        select_stmt: Select[tuple[UUID, str, UserRole, bool]] = (
            select(
                users_table.c.id,
                users_table.c.username,
                users_table.c.role,
                users_table.c.is_active,
            )
            .order_by(order_by)
            .limit(user_list_params.pagination.limit)
            .offset(user_list_params.pagination.offset)
        )

        try:
            result: Result[
                tuple[UUID, str, UserRole, bool]
            ] = await self._session.execute(select_stmt)
            rows: Sequence[Row[tuple[UUID, str, UserRole, bool]]] = result.all()

            return [
                UserQueryModel(
                    id=row.id,
                    username=row.username,
                    role=row.role,
                    is_active=row.is_active,
                )
                for row in rows
            ]

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
