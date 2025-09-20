import logging
from typing import TYPE_CHECKING

from pix_erase.domain.user.values.user_id import UserID
from pix_erase.infrastructure.auth.session.id_generator import AuthSessionIDGenerator
from pix_erase.infrastructure.auth.session.model import AuthSession
from pix_erase.infrastructure.auth.session.ports.gateway import AuthSessionGateway
from pix_erase.infrastructure.auth.session.ports.transaction_manager import AuthSessionTransactionManager
from pix_erase.infrastructure.auth.session.ports.transport import AuthSessionTransport
from pix_erase.infrastructure.auth.session.timer_utc import UtcAuthSessionTimer
from pix_erase.application.errors.auth import AuthenticationError
from pix_erase.infrastructure.errors.transaction_manager import RepoError

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class AuthSessionService:
    def __init__(
        self,
        auth_session_gateway: AuthSessionGateway,
        auth_session_transport: AuthSessionTransport,
        auth_transaction_manager: AuthSessionTransactionManager,
        auth_session_id_generator: AuthSessionIDGenerator,
        auth_session_timer: UtcAuthSessionTimer,
    ) -> None:
        self._auth_session_gateway = auth_session_gateway
        self._auth_session_transport = auth_session_transport
        self._auth_transaction_manager = auth_transaction_manager
        self._auth_session_id_generator = auth_session_id_generator
        self._auth_session_timer = auth_session_timer
        self._cached_auth_session: AuthSession | None = None

    async def create_session(self, user_id: UserID) -> None:
        """
        :raises AuthenticationError:
        """
        log.debug("Create auth session: started. User ID: '%s'.", user_id)

        auth_session_id: str = self._auth_session_id_generator()
        expiration: datetime = self._auth_session_timer.auth_session_expiration
        auth_session = AuthSession(
            id_=auth_session_id,
            user_id=user_id,
            expiration=expiration,
        )

        try:
            self._auth_session_gateway.add(auth_session)
            await self._auth_transaction_manager.commit()

        except RepoError as error:
            msg = "Authentication is currently unavailable. Please try again later."
            raise AuthenticationError(msg) from error

        self._auth_session_transport.deliver(auth_session)

        log.debug(
            "Create auth session: done. User ID: '%s', Auth session id: '%s'.",
            user_id,
            auth_session.id_,
        )

    async def get_authenticated_user_id(self) -> UserID:
        """
        :raises AuthenticationError:
        """
        log.debug("Get authenticated user ID: started.")

        raw_auth_session = await self._load_current_session()
        valid_auth_session = await self._validate_and_extend_session(raw_auth_session)

        log.debug(
            "Get authenticated user ID: done. Auth session ID: %s. User ID: %s.",
            valid_auth_session.id_,
            valid_auth_session.user_id,
        )
        return valid_auth_session.user_id

    async def invalidate_current_session(self) -> None:
        log.debug("Invalidate current session: started. Auth session ID: unknown.")

        auth_session_id: str | None = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            log.warning(
                "Invalidate current session failed: partially failed. "
                "Session ID can't be extracted from transport. "
                "Auth session can't be identified.",
            )
            return

        log.debug(
            "Invalidate current session: in progress. Auth session id: %s.",
            auth_session_id,
        )

        self._auth_session_transport.remove_current()

        auth_session: AuthSession | None = None
        try:
            auth_session = await self._auth_session_gateway.read_by_id(auth_session_id)

        except RepoError:
            log.exception("Auth session extraction failed.")

        if auth_session is None:
            log.warning(
                "Invalidate current session failed: partially failed. "
                "Session ID was removed from transport, "
                "but auth session was not found in storage.",
            )
            return

        try:
            await self._auth_session_gateway.delete(auth_session.id_)
            await self._auth_transaction_manager.commit()

        except RepoError:
            log.warning(
                (
                    "Invalidate current session failed: partially failed. "
                    "Session ID was removed from transport, "
                    "but auth session was not deleted from storage. "
                    "Auth session ID: '%s'."
                ),
                auth_session.id_,
            )

    async def invalidate_all_sessions_for_user(self, user_id: UserID) -> None:
        """
        :raises DataMapperError:
        """
        log.debug(
            "Invalidate all sessions for user: started. User id: '%s'.",
            user_id,
        )

        await self._auth_session_gateway.delete_all_for_user(user_id)
        await self._auth_transaction_manager.commit()

        log.debug(
            "Invalidate all sessions for user: done. User id: '%s'.",
            user_id,
        )

    async def _load_current_session(self) -> AuthSession:
        """
        :raises AuthenticationError:
        """
        log.debug("Load current auth session: started. Auth session id: unknown.")
        if self._cached_auth_session is not None:
            cached_auth_session = self._cached_auth_session
            log.debug(
                "Load current auth session: done (from cache). Auth session id: %s.",
                cached_auth_session.id_,
            )
            return cached_auth_session

        auth_session_id: str | None = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            log.debug("Session not found.")
            msg = "Not authenticated."
            raise AuthenticationError(msg)

        log.debug(
            "Load current auth session: in progress. Auth session id: %s.",
            auth_session_id,
        )

        try:
            auth_session: AuthSession | None = await self._auth_session_gateway.read_by_id(
                auth_session_id,
            )
        except RepoError as error:
            log.exception("Auth session extraction failed.")
            msg = "Not authenticated."
            raise AuthenticationError(msg) from error

        if auth_session is None:
            log.debug("Session not found.")
            msg = "Not authenticated."
            raise AuthenticationError(msg)

        self._cached_auth_session = auth_session

        log.debug(
            "Load current auth session: done. Auth session id: %s.",
            auth_session.id_,
        )
        return auth_session

    async def _validate_and_extend_session(
        self,
        auth_session: AuthSession,
    ) -> AuthSession:
        """
        :raises AuthenticationError:
        """
        log.debug(
            "Validate and extend auth session: started. Auth session id: %s.",
            auth_session.id_,
        )

        now = self._auth_session_timer.current_time
        if auth_session.expiration <= now:
            log.debug("Session expired.")
            msg = "Not authenticated."
            raise AuthenticationError(msg)

        if auth_session.expiration - now > self._auth_session_timer.refresh_trigger_interval:
            log.debug(
                "Validate and extend auth session: validated without extension. Auth session id: %s.",
                auth_session.id_,
            )
            return auth_session

        original_expiration = auth_session.expiration
        auth_session.expiration = self._auth_session_timer.auth_session_expiration

        try:
            await self._auth_session_gateway.update(auth_session)
            await self._auth_transaction_manager.commit()

        except RepoError:
            log.exception("Auth session extension failed.")
            auth_session.expiration = original_expiration
            return auth_session

        self._auth_session_transport.deliver(auth_session)

        self._cached_auth_session = auth_session

        log.debug(
            "Validate and extend auth session: done. Auth session id: %s.",
            auth_session.id_,
        )
        return auth_session