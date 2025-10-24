from inspect import getdoc
from typing import Final
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Security

from pix_erase.application.commands.internet_protocol.scan_common_ports import (
    ScanCommonPortsCommand,
    ScanCommonPortsCommandHandler,
)
from pix_erase.application.commands.internet_protocol.scan_port import (
    ScanPortCommand,
    ScanPortCommandHandler,
)
from pix_erase.application.commands.internet_protocol.scan_port_range import (
    ScanPortRangeCommand,
    ScanPortRangeCommandHandler,
)
from pix_erase.application.commands.internet_protocol.scan_ports import (
    ScanPortsCommand,
    ScanPortsCommandHandler,
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

router: Final[APIRouter] = APIRouter(
    prefix="/scan-ports",
    tags=["IP"],
    route_class=DishkaRoute
)


@router.post(
    "/single/",
    response_model=PortScanResultResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Scan a single port",
    description=getdoc(ScanPortCommandHandler),
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
async def scan_port(
        request: PortScanRequestSchema,
        handler: FromDishka[ScanPortCommandHandler],
) -> PortScanResultResponseSchema:
    command: ScanPortCommand = ScanPortCommand(
        target=request.target,
        port=request.port,
        timeout=request.timeout,
    )

    result: PortScanView = await handler(command)

    response: PortScanResultResponseSchema = PortScanResultResponseSchema(
        port=result.port,
        status=result.status,
        response_time=result.response_time,
        service=result.service,
        error_message=result.error_message,
        scanned_at=result.scanned_at,
    )

    return response


@router.post(
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
async def scan_ports(
        request: PortScanMultipleRequest,
        handler: FromDishka[ScanPortsCommandHandler],
) -> list[PortScanResultResponseSchema]:
    command: ScanPortsCommand = ScanPortsCommand(
        target=request.target,
        ports=request.ports,
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    results: list[PortScanView] = await handler(command)

    response: list[PortScanResultResponseSchema] = [
        PortScanResultResponseSchema(
            port=result.port,
            status=result.status,
            response_time=result.response_time,
            service=result.service,
            error_message=result.error_message,
            scanned_at=result.scanned_at,
        )
        for result in results
    ]

    return response


@router.post(
    "/range/",
    response_model=PortScanSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Scan a range of ports",
    description=getdoc(ScanPortRangeCommandHandler),
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
async def scan_port_range(
        request: PortScanRangeRequest,
        handler: FromDishka[ScanPortRangeCommandHandler],
) -> PortScanSummaryResponse:
    command: ScanPortRangeCommand = ScanPortRangeCommand(
        target=request.target,
        start_port=request.start_port,
        end_port=request.end_port,
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    result: PortScanSummaryView = await handler(command)

    response: PortScanSummaryResponse = PortScanSummaryResponse(
        target=result.target,
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


@router.post(
    "/common/",
    response_model=PortScanSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Scan common ports",
    description=getdoc(ScanCommonPortsCommandHandler),
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
async def scan_common_ports(
        request: PortScanCommonRequest,
        handler: FromDishka[ScanCommonPortsCommandHandler],
) -> PortScanSummaryResponse:
    command: ScanCommonPortsCommand = ScanCommonPortsCommand(
        target=request.target,
        timeout=request.timeout,
        max_concurrent=request.max_concurrent,
    )

    result: PortScanSummaryView = await handler(command)

    response: PortScanSummaryResponse = PortScanSummaryResponse(
        target=result.target,
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
