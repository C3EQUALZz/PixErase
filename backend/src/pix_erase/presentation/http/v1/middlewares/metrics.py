import time

from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

from pix_erase.infrastructure.metrics.manager import MetricsManager
from pix_erase.infrastructure.tracing.integrations.fastapi import get_path


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            metrics: MetricsManager,
            *,
            include_trace_exemplar: bool,
    ) -> None:
        super().__init__(app)
        self.metrics = metrics
        self.include_exemplar = include_trace_exemplar

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.scope["type"] != "http":
            return await call_next(request)

        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        method = request.method
        path, is_handled_path = get_path(request)

        if not is_handled_path:
            return await call_next(request)

        before_time = time.perf_counter()
        self.metrics.inc_requests_count(method=method, path=path)
        self.metrics.add_request_in_progress(method=method, path=path)

        try:
            response = await call_next(request)
        except Exception as exc:
            self.metrics.inc_requests_exceptions_count(
                method=method,
                path=path,
                exception_type=type(exc).__name__,
            )
            raise
        else:
            after_time = time.perf_counter()
            status_code = response.status_code
            exemplar: dict[str, str] | None = None

            if self.include_exemplar:
                span = trace.get_current_span()
                trace_id = trace.format_trace_id(span.get_span_context().trace_id)
                exemplar = {"TraceID": trace_id}

            self.metrics.observe_request_duration(
                method=method,
                path=path,
                duration=after_time - before_time,
                exemplar=exemplar,
            )
        finally:
            self.metrics.inc_responses_count(method=method, path=path, status_code=status_code)
            self.metrics.remove_request_in_progress(method=method, path=path)

        return response
