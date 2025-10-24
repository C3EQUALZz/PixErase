from starlette.requests import Request
from starlette.responses import Response

from pix_erase.infrastructure.metrics.route import get_latest_metrics


async def get_metrics(request: Request) -> Response:
    registry = request.app.state.metrics_registry
    openmetrics_format = request.app.state.openmetrics_format
    response = get_latest_metrics(registry, openmetrics_format=openmetrics_format)
    return Response(
        content=response.payload,
        status_code=response.status_code,
        headers=response.headers,
    )
