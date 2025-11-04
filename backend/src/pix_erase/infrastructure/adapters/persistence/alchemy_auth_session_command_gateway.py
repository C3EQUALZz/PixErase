from typing import Final, override

from sqlalchemy import Delete, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pix_erase.domain.user.values.user_id import UserID
from pix_erase.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from pix_erase.infrastructure.auth.session.model import AuthSession
from pix_erase.infrastructure.auth.session.ports.gateway import AuthSessionGateway
from pix_erase.infrastructure.errors.transaction_manager import RepoError


class SQLAlchemyAuthSessionCommandGateway(AuthSessionGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, auth_session: AuthSession) -> None:
        try:
            self._session.add(auth_session)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_by_id(self, auth_session_id: str) -> AuthSession | None:
        try:
            auth_session: AuthSession | None = await self._session.get(
                AuthSession,
                auth_session_id,
            )

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return auth_session

    @override
    async def update(self, auth_session: AuthSession) -> None:
        try:
            await self._session.merge(auth_session)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def delete(self, auth_session_id: str) -> None:
        delete_stmt: Delete = delete(AuthSession).where(
            AuthSession.user_id == auth_session_id,  # type: ignore
        )

        try:
            await self._session.execute(delete_stmt)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def delete_all_for_user(self, user_id: UserID) -> None:
        delete_stmt: Delete = delete(AuthSession).where(
            AuthSession.user_id == user_id,  # type: ignore
        )

        try:
            await self._session.execute(delete_stmt)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
