from datetime import UTC, datetime, timedelta
from typing import Final, NewType

AuthSessionTtlMin = NewType("AuthSessionTtlMin", timedelta)
AuthSessionRefreshThreshold = NewType("AuthSessionRefreshThreshold", float)


class UtcAuthSessionTimer:
    def __init__(
        self,
        auth_session_ttl_min: AuthSessionTtlMin,
        auth_session_refresh_threshold: AuthSessionRefreshThreshold,
    ) -> None:
        self._auth_session_ttl_min: Final[AuthSessionTtlMin] = auth_session_ttl_min
        self._auth_session_refresh_threshold: Final[AuthSessionRefreshThreshold] = auth_session_refresh_threshold

    @property
    def current_time(self) -> datetime:
        return datetime.now(tz=UTC)

    @property
    def auth_session_expiration(self) -> datetime:
        return self.current_time + self._auth_session_ttl_min

    @property
    def refresh_trigger_interval(self) -> timedelta:
        return self._auth_session_ttl_min * self._auth_session_refresh_threshold
