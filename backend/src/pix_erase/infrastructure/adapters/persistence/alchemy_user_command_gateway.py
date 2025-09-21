from sqlalchemy import Delete, delete, select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from pix_erase.infrastructure.errors.transaction_manager import RepoError


class SqlAlchemyUserCommandGateway(UserCommandGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def add(self, user: User) -> None:
        try:
            self._session.add(user)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_by_id(self, user_id: UserID) -> User | None:
        select_stmt: Select[tuple[User]] = select(User).where(User.id == user_id)  # type: ignore

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_by_email(self, email: UserEmail) -> User | None:
        select_stmt: Select[tuple[User]] = select(User).where(User.email == email)  # type: ignore

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def delete_by_id(self, user_id: UserID) -> None:
        delete_stm: Delete = delete(User).where(User.id == user_id)  # type: ignore

        try:
            await self._session.execute(delete_stm)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

