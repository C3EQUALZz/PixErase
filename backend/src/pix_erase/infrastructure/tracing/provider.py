from typing import Any

from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.util.http import get_excluded_urls

from pix_erase.setup.config.tracing import BaseTracingConfig


def build_open_telemetry_middleware(app: Any, config: BaseTracingConfig) -> OpenTelemetryMiddleware:
    return OpenTelemetryMiddleware(
        app=app,
        client_request_hook=config.client_request_hook_handler,
        client_response_hook=config.client_response_hook_handler,
        default_span_details=config.scope_span_details_extractor,
        excluded_urls=get_excluded_urls(config.exclude_urls_env_key),
        meter=config.meter,
        meter_provider=config.meter_provider,
        server_request_hook=config.server_request_hook_handler,
        tracer_provider=config.tracer_provider,
    )