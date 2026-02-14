import logging
from typing import Final

from grpc import ServicerContext

from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtAccessTokenProcessor
from pix_erase.infrastructure.auth.session.model import AuthSession
from pix_erase.infrastructure.auth.session.ports.transport import AuthSessionTransport

log: Final[logging.Logger] = logging.getLogger(__name__)

METADATA_ACCESS_TOKEN_KEY: Final[str] = "authorization"  # noqa: S105
METADATA_BEARER_PREFIX: Final[str] = "Bearer "
METADATA_SET_TOKEN_KEY: Final[str] = "set-access-token"  # noqa: S105
METADATA_DELETE_TOKEN_KEY: Final[str] = "delete-access-token"  # noqa: S105


class JwtGrpcMetadataAuthSessionTransport(AuthSessionTransport):
    def __init__(
        self,
        context: ServicerContext,
        access_token_processor: JwtAccessTokenProcessor,
    ) -> None:
        self._context: Final[ServicerContext] = context
        self._access_token_processor: Final[JwtAccessTokenProcessor] = access_token_processor

    def deliver(self, auth_session: AuthSession) -> None:
        access_token: str = self._access_token_processor.encode(auth_session)
        self._context.set_trailing_metadata(
            ((METADATA_SET_TOKEN_KEY, access_token),),
        )
        log.debug("Delivered auth session token via gRPC trailing metadata. Session ID: %s", auth_session.id_)

    def extract_id(self) -> str | None:
        metadata = self._context.invocation_metadata()
        if metadata is None:
            log.debug("No invocation metadata found.")
            return None

        for key, value in metadata:
            if key == METADATA_ACCESS_TOKEN_KEY:
                token = value.removeprefix(METADATA_BEARER_PREFIX)
                return self._access_token_processor.decode_auth_session_id(token)

        log.debug("No access token found in gRPC metadata.")
        return None

    def remove_current(self) -> None:
        self._context.set_trailing_metadata(
            ((METADATA_DELETE_TOKEN_KEY, "true"),),
        )
        log.debug("Marked access token for removal via gRPC trailing metadata.")
