from typing import Any

from opentelemetry.semconv.trace import SpanAttributes
from starlette.requests import Request
from starlette.routing import Match
from starlette.types import Scope


def get_route_details(scope: Scope) -> str | None:
    app = scope["app"]
    route = None

    for starlette_route in app.routes:
        match, _ = starlette_route.matches(scope)
        if match == Match.FULL:
            route = starlette_route.path
            break
        if match == Match.PARTIAL:
            route = starlette_route.path
    return route


def get_default_span_details(scope: Scope) -> tuple[str, dict[str, Any]]:
    route = get_route_details(scope)
    method = scope.get("method", "")
    attributes = {}
    if route:
        attributes[SpanAttributes.HTTP_ROUTE] = route
    if method and route:  # http
        span_name = f"{method} {route}"
    else:  # fallback
        span_name = method
    return span_name, attributes


def get_path(request: Request) -> tuple[str, bool]:
    for route in request.app.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return route.path, True
    return request.url.path, False
