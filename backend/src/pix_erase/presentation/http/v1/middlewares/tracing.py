from typing import Final

from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send

from pix_erase.infrastructure.tracing.provider import build_open_telemetry_middleware
from pix_erase.setup.config.tracing import FastAPITracingConfig


class TracingMiddleware:
    __slots__ = ("app", "open_telemetry_middleware")

    def __init__(self, app: ASGIApp, config: FastAPITracingConfig) -> None:
        self.app: Final[ASGIApp] = app
        self.open_telemetry_middleware: Final[OpenTelemetryMiddleware] = build_open_telemetry_middleware(app, config)

    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send,
    ) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        return await self.open_telemetry_middleware(scope, receive, send)  # type: ignore[arg-type]
