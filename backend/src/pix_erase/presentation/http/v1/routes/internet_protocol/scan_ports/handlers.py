from inspect import getdoc
from typing import Final, cast, Literal, TYPE_CHECKING, Annotated
from datetime import datetime, UTC
from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Security
from fastapi.params import Depends
from opentelemetry import trace
from opentelemetry.trace import Tracer

if TYPE_CHECKING:
    from pydantic import IPvAnyAddress

from pix_erase.application.queries.internet_protocol.scan_common_ports import (
    ScanCommonPortsQuery,
    ScanCommonPortsQueryHandler,
)
from pix_erase.application.queries.internet_protocol.scan_port import (
    ScanPortQuery,
    ScanPortQueryHandler,
)
from pix_erase.application.queries.internet_protocol.scan_port_range import (
    ScanPortRangeQuery,
    ScanPortRangeQueryHandler,
)
from pix_erase.application.queries.internet_protocol.scan_ports import (
    ScanPortsQuery,
    ScanPortsQueryHandler,
)
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanSummaryView, PortScanView
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

from pix_erase.presentation.http.v1.routes.internet_protocol.scan_ports.schemas import (
    PortScanRequestSchema,
    PortScanMultipleRequest,
    PortScanRangeRequest,
    PortScanCommonRequest,
    PortScanResultResponseSchema,
    PortScanSummaryResponse,
)

scan_ports_router: Final[APIRouter] = APIRouter(
    prefix="/scan-ports",
    tags=["IP"],
    route_class=DishkaRoute
)
tracer: Final[Tracer] = trace.get_tracer(__name__)


@scan_ports_router.get(
    "/single/",
    response_model=PortScanResultResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Scan a single port",
    description=getdoc(ScanPortQueryHandler),
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
    name="span ip scan_port http",
    attributes={
        "http.request.method": "POST",
        "url.path": "/ip/scan-ports/single/",
        "http.route": "/ip/scan-ports/single/",
        "feature": "ip",
        "action": "scan_port",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def scan_port(
        request: Annotated[PortScanRequestSchema, Depends()],
        handler: FromDishka[ScanPortQueryHandler],
) -> PortScanResultResponseSchema:
    command: ScanPortQuery = ScanPortQuery(
        target=str(request.target),
        port=request.port,
        timeout=request.timeout,
    )

    result: PortScanView = await handler(command)

    response: PortScanResultResponseSchema = PortScanResultResponseSchema(
        port=result.port,
        status=cast(Literal["open", "closed"], result.status),
        response_time=result.response_time,
        service=result.service,
        error_message=result.error_message,
        scanned_at=result.scanned_at,
    )

    return response


@scan_ports_router.get(
    "/multiple/",
    response_model=list[PortScanResultResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Scan multiple ports",
    description="Scan multiple ports on a target IP address or hostname",
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
    name="span ip scan_ports http",
    attributes={
        "http.request.method": "POST",
        "url.path": "/ip/scan-ports/multiple/",
        "http.route": "/ip/scan-ports/multiple/",
        "feature": "ip",
        "action": "scan_ports",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def scan_ports(
        request: Annotated[PortScanMultipleRequest, Depends()],
        handler: FromDishka[ScanPortsQueryHandler],
) -> list[PortScanResultResponseSchema]:
    command: ScanPortsQuery = ScanPortsQuery(
        target=str(request.target),
        ports=request.ports,
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    results: list[PortScanView] = await handler(command)

    response: list[PortScanResultResponseSchema] = [
        PortScanResultResponseSchema(
            port=result.port,
            status=cast(Literal["open", "closed"], result.status),
            response_time=result.response_time,
            service=result.service,
            error_message=result.error_message,
            scanned_at=result.scanned_at,
        )
        for result in results
    ]

    return response


@scan_ports_router.post(
    "/range/",
    response_model=PortScanSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Scan a range of ports",
    description=getdoc(ScanPortRangeQueryHandler),
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
    name="span ip scan_port_range http",
    attributes={
        "http.request.method": "POST",
        "url.path": "/ip/scan-ports/range/",
        "http.route": "/ip/scan-ports/range/",
        "feature": "ip",
        "action": "scan_port_range",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def scan_port_range(
        request: Annotated[PortScanRangeRequest, Depends()],
        handler: FromDishka[ScanPortRangeQueryHandler],
) -> PortScanSummaryResponse:
    command: ScanPortRangeQuery = ScanPortRangeQuery(
        target=str(request.target),
        start_port=request.start_port,
        end_port=request.end_port,
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    result: PortScanSummaryView = await handler(command)

    response: PortScanSummaryResponse = PortScanSummaryResponse(
        target=cast("IPvAnyAddress", result.target),
        port_range=result.port_range,
        total_ports=result.total_ports,
        open_ports=result.open_ports,
        closed_ports=result.closed_ports,
        filtered_ports=result.filtered_ports,
        scan_duration=result.scan_duration,
        started_at=result.started_at,
        completed_at=result.completed_at,
        success_rate=result.success_rate,
        results=[
            PortScanResultResponseSchema(
                port=res["port"],
                status=res["status"],
                response_time=res["response_time"],
                service=res["service"],
                error_message=res["error_message"],
                scanned_at=res["scanned_at"],
            )
            for res in result.results
        ],
    )

    return response


@scan_ports_router.get(
    "/common/",
    response_model=PortScanSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Scan common ports",
    description=getdoc(ScanCommonPortsQueryHandler),
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
    name="span ip scan_common_ports http",
    attributes={
        "http.request.method": "POST",
        "url.path": "/ip/scan-ports/common/",
        "http.route": "/ip/scan-ports/common/",
        "feature": "ip",
        "action": "scan_common_ports",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def scan_common_ports(
        request: Annotated[PortScanCommonRequest, Depends()],
        handler: FromDishka[ScanCommonPortsQueryHandler],
) -> PortScanSummaryResponse:
    command: ScanCommonPortsQuery = ScanCommonPortsQuery(
        target=str(request.target),
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    result: PortScanSummaryView = await handler(command)

    response: PortScanSummaryResponse = PortScanSummaryResponse(
        target=cast("IPvAnyAddress", result.target),
        port_range=result.port_range,
        total_ports=result.total_ports,
        open_ports=result.open_ports,
        closed_ports=result.closed_ports,
        filtered_ports=result.filtered_ports,
        scan_duration=result.scan_duration,
        started_at=result.started_at,
        completed_at=result.completed_at,
        success_rate=result.success_rate,
        results=[
            PortScanResultResponseSchema(
                port=res["port"],
                status=res["status"],
                response_time=res["response_time"],
                service=res["service"],
                error_message=res["error_message"],
                scanned_at=res["scanned_at"],
            )
            for res in result.results
        ],
    )

    return response
