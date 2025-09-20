import logging
from typing import Any, Final, Literal, NewType, TypedDict, cast

import jwt

from automatic_responses.infrastructure.auth.session.model import AuthSession

logger: Final[logging.Logger] = logging.getLogger(__name__)

JwtSecret = NewType("JwtSecret", str)
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]


class JwtPayload(TypedDict):
    auth_session_id: str
    exp: int


class JwtAccessTokenProcessor:
    def __init__(self, secret: JwtSecret, algorithm: JwtAlgorithm) -> None:
        self._secret: Final[JwtSecret] = secret
        self._algorithm: Final[JwtAlgorithm] = algorithm

    def encode(self, auth_session: AuthSession) -> str:
        payload: JwtPayload = JwtPayload(
            auth_session_id=auth_session.id_,
            exp=int(auth_session.expiration.timestamp()),
        )

        return jwt.encode(
            cast("dict[str, Any]", payload),
            key=self._secret,
            algorithm=self._algorithm,
        )

    def decode_auth_session_id(self, token: str) -> str | None:
        try:
            payload: dict[str, Any] = cast(
                "dict[str, Any]",
                jwt.decode(
                    token,
                    key=self._secret,
                    algorithms=[self._algorithm],
                ),
            )

        except jwt.PyJWTError as error:
            logger.debug("Invalid or expired JWT. %s", error)
            return None

        auth_session_id: str | None = payload.get("auth_session_id")

        if auth_session_id is None:
            logger.debug("JWT payload missing. 'auth_session_id'")
            return None

        return auth_session_id