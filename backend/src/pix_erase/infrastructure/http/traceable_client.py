from typing import Any, Final, MutableMapping, override

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.trace import SpanKind, Status, StatusCode

from pix_erase.infrastructure.http.base import HttpClient, HttpHeaders, HttpResponse, QueryParams

tracer: Final[trace.Tracer] = trace.get_tracer(__name__)


class TraceableHttpClient(HttpClient):
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client: Final[HttpClient] = http_client

    @override
    async def get(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        span_name = "http.client GET"
        with tracer.start_as_current_span(span_name, kind=SpanKind.CLIENT) as span:
            _set_common_request_attributes(span, method="GET", url=url, params=params, timeout=timeout)
            injected_headers = _prepare_headers_with_context(headers)
            try:
                response = await self._http_client.get(
                    url,
                    params=params,
                    headers=injected_headers,
                    timeout=timeout,
                )
                _set_response_attributes(span, response)
                return response
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def post(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        json_like: Any | None = None,
        data: Any | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        span_name = "http.client POST"
        with tracer.start_as_current_span(span_name, kind=SpanKind.CLIENT) as span:
            _set_common_request_attributes(span, method="POST", url=url, params=params, timeout=timeout)
            if json_like is not None:
                span.set_attribute("http.request.body.size_hint", len(json_like))
            if data is not None and isinstance(data, (bytes, str)):
                span.set_attribute("http.request.body.size", len(data))
            injected_headers = _prepare_headers_with_context(headers)
            try:
                response = await self._http_client.post(
                    url,
                    params=params,
                    headers=injected_headers,
                    json_like=json_like,
                    data=data,
                    timeout=timeout,
                )
                _set_response_attributes(span, response)
                return response
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def put(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        json_like: Any | None = None,
        data: Any | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        span_name = "http.client PUT"
        with tracer.start_as_current_span(span_name, kind=SpanKind.CLIENT) as span:
            _set_common_request_attributes(span, method="PUT", url=url, params=params, timeout=timeout)
            injected_headers = _prepare_headers_with_context(headers)
            try:
                response = await self._http_client.put(
                    url,
                    params=params,
                    headers=injected_headers,
                    json_like=json_like,
                    data=data,
                    timeout=timeout,
                )
                _set_response_attributes(span, response)
                return response
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def delete(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        span_name = "http.client DELETE"
        with tracer.start_as_current_span(span_name, kind=SpanKind.CLIENT) as span:
            _set_common_request_attributes(span, method="DELETE", url=url, params=params, timeout=timeout)
            injected_headers = _prepare_headers_with_context(headers)
            try:
                response = await self._http_client.delete(
                    url,
                    params=params,
                    headers=injected_headers,
                    timeout=timeout,
                )
                _set_response_attributes(span, response)
                return response
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise


def _prepare_headers_with_context(headers: HttpHeaders | None) -> MutableMapping[str, str]:
    # Create a mutable copy for propagation
    out: MutableMapping[str, str]
    if headers is None:
        out = {}
    else:
        out = dict(headers)
    inject(out)
    return out


def _set_common_request_attributes(span: trace.Span, *, method: str, url: str, params: QueryParams | None, timeout: float | None) -> None:
    span.set_attribute("external_http.request.method", method)
    span.set_attribute("url.full", url)
    if timeout is not None:
        span.set_attribute("timeout.ms", int(timeout * 1000))
    if params is not None:
        try:
            if isinstance(params, dict):
                span.set_attribute("http.request.params.count", len(params))
            elif isinstance(params, (list, tuple)):
                span.set_attribute("http.request.params.count", len(params))
        except Exception:  # noqa: BLE001
            pass


def _set_response_attributes(span: trace.Span, response: HttpResponse) -> None:
    span.set_attribute("http.response.status_code", response.status_code)
    span.set_attribute("network.protocol.name", "http")
    span.set_attribute("server.address", response.url)
    if response.content is not None:
        span.set_attribute("http.response.body.size", len(response.content))
    if 400 <= response.status_code:
        span.set_status(Status(StatusCode.ERROR))





