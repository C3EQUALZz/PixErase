from typing import Final

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer
from typing_extensions import override

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_params.user_filters import UserListParams
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_id import UserID

tracer: Final[Tracer] = trace.get_tracer(__name__)


class TraceableUserQueryGateway(UserQueryGateway):
    def __init__(self, user_query_gateway: UserQueryGateway) -> None:
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway

    @override
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        span_name = "user.query_gateway.read_user_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "read_user_by_id")
            span.set_attribute("user.id", str(user_id))
            try:
                user = await self._user_query_gateway.read_user_by_id(user_id)
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
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        span_name = "user.query_gateway.read_all_users"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.operation", "read_all_users")
            _set_user_list_params_attributes(span, user_list_params)
            try:
                users = await self._user_query_gateway.read_all_users(user_list_params)
                if users is not None:
                    span.set_attribute("db.query.result.count", len(users))
                    span.set_attribute("db.query.result.found", True)
                else:
                    span.set_attribute("db.query.result.found", False)
                    span.set_attribute("db.query.result.count", 0)
                span.set_status(Status(StatusCode.OK))
                return users
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


def _set_user_list_params_attributes(span: trace.Span, user_list_params: UserListParams) -> None:
    """Set user list query parameters attributes on a span."""
    span.set_attribute("db.query.sorting.field", user_list_params.sorting.sorting_field)
    span.set_attribute("db.query.sorting.order", user_list_params.sorting.sorting_order)
    span.set_attribute("db.query.pagination.limit", user_list_params.pagination.limit)
    span.set_attribute("db.query.pagination.offset", user_list_params.pagination.offset)

