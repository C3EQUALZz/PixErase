from typing import Final

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer
from typing_extensions import override

from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID

tracer: Final[Tracer] = trace.get_tracer(__name__)


class TraceableUserCommandGateway(UserCommandGateway):
    def __init__(self, user_command_gateway: UserCommandGateway) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway

    @override
    async def add(self, user: User) -> None:
        span_name = "user.command_gateway.add"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_user_attributes(span, user)
            span.set_attribute("db.operation", "add")
            try:
                await self._user_command_gateway.add(user)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def read_by_id(self, user_id: UserID) -> User | None:
        span_name = "user.command_gateway.read_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "read_by_id")
            span.set_attribute("user.id", str(user_id))
            try:
                user = await self._user_command_gateway.read_by_id(user_id)
                if user is not None:
                    _set_user_attributes(span, user)
                    span.set_attribute("db.query.result.found", True)
                else:
                    span.set_attribute("db.query.result.found", False)
                span.set_status(Status(StatusCode.OK))
                return user
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def read_by_email(self, email: UserEmail) -> User | None:
        span_name = "user.command_gateway.read_by_email"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "read_by_email")
            span.set_attribute("user.email", str(email))
            try:
                user = await self._user_command_gateway.read_by_email(email)
                if user is not None:
                    _set_user_attributes(span, user)
                    span.set_attribute("db.query.result.found", True)
                else:
                    span.set_attribute("db.query.result.found", False)
                span.set_status(Status(StatusCode.OK))
                return user
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def delete_by_id(self, user_id: UserID) -> None:
        span_name = "user.command_gateway.delete_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "delete_by_id")
            span.set_attribute("user.id", str(user_id))
            try:
                await self._user_command_gateway.delete_by_id(user_id)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def update(self, user: User) -> None:
        span_name = "user.command_gateway.update"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_user_attributes(span, user)
            span.set_attribute("db.operation", "update")
            try:
                await self._user_command_gateway.update(user)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise


def _set_user_attributes(span: trace.Span, user: User) -> None:
    """Set user-related attributes on a span."""
    span.set_attribute("user.id", str(user.id))
    span.set_attribute("user.email", str(user.email))
    span.set_attribute("user.name", str(user.name))
    span.set_attribute("user.role", user.role)
    span.set_attribute("user.is_active", user.is_active)
    span.set_attribute("user.images.count", len(user.images))

