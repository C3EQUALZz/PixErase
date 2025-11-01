from typing import Final, Annotated
from inspect import getdoc
from datetime import datetime, UTC
from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Depends, Security
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.queries.internet_protocol.ping_internet_protocol import (
    PingInternetProtocolQueryHandler,
    PingInternetProtocolQuery
)
from pix_erase.application.common.views.internet_protocol.ping_internet_protocol import PingInternetProtocolView
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.internet_protocol.ping.schemas import PingSchemaRequest, PingSchemaResponse

ip_ping_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["IP"]
)
tracer: Final[Tracer] = trace.get_tracer(__name__)


@ip_ping_router.get(
    "/ping/",
    status_code=status.HTTP_200_OK,
    summary="Ping service with known ip",
    response_model=PingSchemaResponse,
    description=getdoc(PingInternetProtocolQueryHandler),
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_408_REQUEST_TIMEOUT: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
@span(
    tracer=tracer,
    name="span ip ping http",
    attributes={
        "http.request.method": "GET",
        "url.path": "/ip/ping/",
        "http.route": "/ip/ping/",
        "feature": "ip",
        "action": "ping",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def ping_handler(
        request_schema: Annotated[PingSchemaRequest, Depends()],
        interactor: FromDishka[PingInternetProtocolQueryHandler]
) -> PingSchemaResponse:
    command: PingInternetProtocolQuery = PingInternetProtocolQuery(
        destination_address=str(request_schema.destination_address),
        timeout=request_schema.timeout,
        packet_size=request_schema.packet_size,
        ttl=request_schema.ttl,
    )

    view: PingInternetProtocolView = await interactor(command)

    return PingSchemaResponse(
        success=view.success,
        response_time_ms=view.response_time_ms,
        error_message=view.error_message,
        ttl=view.ttl,
        packet_size=view.packet_size,
    )
