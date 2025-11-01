from typing import Final

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer
from typing_extensions import override

from pix_erase.domain.user.values.user_id import UserID
from pix_erase.infrastructure.auth.session.model import AuthSession
from pix_erase.infrastructure.auth.session.ports.gateway import AuthSessionGateway

tracer: Final[Tracer] = trace.get_tracer(__name__)


class TraceableAuthSessionGateway(AuthSessionGateway):
    def __init__(self, auth_session_gateway: AuthSessionGateway) -> None:
        self._auth_session_gateway: Final[AuthSessionGateway] = auth_session_gateway

    @override
    async def add(self, auth_session: AuthSession) -> None:
        span_name = "auth_session.gateway.add"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_auth_session_attributes(span, auth_session)
            span.set_attribute("db.operation", "add")
            try:
                await self._auth_session_gateway.add(auth_session)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def read_by_id(self, auth_session_id: str) -> AuthSession | None:
        span_name = "auth_session.gateway.read_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "read_by_id")
            span.set_attribute("auth_session.id", auth_session_id)
            try:
                auth_session = await self._auth_session_gateway.read_by_id(auth_session_id)
                if auth_session is not None:
                    _set_auth_session_attributes(span, auth_session)
                    span.set_attribute("db.query.result.found", True)
                else:
                    span.set_attribute("db.query.result.found", False)
                span.set_status(Status(StatusCode.OK))
                return auth_session
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def update(self, auth_session: AuthSession) -> None:
        span_name = "auth_session.gateway.update"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_auth_session_attributes(span, auth_session)
            span.set_attribute("db.operation", "update")
            try:
                await self._auth_session_gateway.update(auth_session)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def delete(self, auth_session_id: str) -> None:
        span_name = "auth_session.gateway.delete"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "delete")
            span.set_attribute("auth_session.id", auth_session_id)
            try:
                await self._auth_session_gateway.delete(auth_session_id)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def delete_all_for_user(self, user_id: UserID) -> None:
        span_name = "auth_session.gateway.delete_all_for_user"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "delete_all_for_user")
            span.set_attribute("user.id", str(user_id))
            try:
                await self._auth_session_gateway.delete_all_for_user(user_id)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise


def _set_auth_session_attributes(span: trace.Span, auth_session: AuthSession) -> None:
    """Set auth session-related attributes on a span."""
    span.set_attribute("auth_session.id", auth_session.id_)
    span.set_attribute("user.id", str(auth_session.user_id))
    span.set_attribute("auth_session.expiration", auth_session.expiration.isoformat())

