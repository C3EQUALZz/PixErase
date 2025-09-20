import logging
from typing import Final, override

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pix_erase.infrastructure.adapters.persistence.constants import (
    DB_COMMIT_DONE,
    DB_COMMIT_FAILED,
    DB_CONFLICT,
    DB_QUERY_FAILED,
)
from pix_erase.infrastructure.auth.session.ports.transaction_manager import AuthSessionTransactionManager
from pix_erase.infrastructure.errors.transaction_manager import EntityAddError, RepoError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SqlaAuthSessionTransactionManager(AuthSessionTransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def commit(self) -> None:
        try:
            await self._session.commit()
            logger.debug("%s. Auth session.", DB_COMMIT_DONE)
        except IntegrityError as e:
            logger.exception(DB_CONFLICT)
            raise EntityAddError(DB_CONFLICT) from e
        except SQLAlchemyError as error:
            msg: str = f"{DB_QUERY_FAILED} {DB_COMMIT_FAILED}"
            raise RepoError(msg) from error
