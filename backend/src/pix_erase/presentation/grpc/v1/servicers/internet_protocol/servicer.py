import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject

from pix_erase.application.queries.internet_protocol.analyze_domain_info import (
    AnalyzeDomainQuery,
    AnalyzeDomainQueryHandler,
)
from pix_erase.application.queries.internet_protocol.ping_internet_protocol import (
    PingInternetProtocolQuery,
    PingInternetProtocolQueryHandler,
)
from pix_erase.application.queries.internet_protocol.read_ip_info import ReadIPInfoQuery, ReadIPInfoQueryHandler
from pix_erase.application.queries.internet_protocol.scan_common_ports import (
    ScanCommonPortsQuery,
    ScanCommonPortsQueryHandler,
)
from pix_erase.application.queries.internet_protocol.scan_port import ScanPortQuery, ScanPortQueryHandler
from pix_erase.application.queries.internet_protocol.scan_port_range import (
    ScanPortRangeQuery,
    ScanPortRangeQueryHandler,
)
from pix_erase.application.queries.internet_protocol.scan_ports import ScanPortsQuery, ScanPortsQueryHandler
from pix_erase.presentation.grpc.v1.generated.v1 import internet_protocol_pb2, internet_protocol_pb2_grpc


def _port_scan_view_to_proto(
    view: object,
) -> internet_protocol_pb2.PortScanResultResponse:
    return internet_protocol_pb2.PortScanResultResponse(
        port=view.port,  # type: ignore[attr-defined]
        status=view.status,  # type: ignore[attr-defined]
        response_time=view.response_time,  # type: ignore[attr-defined]
        service=view.service,  # type: ignore[attr-defined]
        error_message=view.error_message,  # type: ignore[attr-defined]
        scanned_at=view.scanned_at.isoformat() if view.scanned_at else None,  # type: ignore[attr-defined]
    )


class InternetProtocolServiceServicer(internet_protocol_pb2_grpc.InternetProtocolServiceServicer):
    @inject
    async def Ping(  # noqa: N802
        self,
        request: internet_protocol_pb2.PingRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[PingInternetProtocolQueryHandler],
    ) -> internet_protocol_pb2.PingResponse:
        query = PingInternetProtocolQuery(
            destination_address=request.destination_address,
            timeout=request.timeout or 4.0,
            packet_size=request.packet_size or 56,
            ttl=request.ttl if request.HasField("ttl") else None,
        )
        view = await handler(query)
        return internet_protocol_pb2.PingResponse(
            success=view.success,
            response_time_ms=view.response_time_ms,
            error_message=view.error_message,
            ttl=view.ttl,
            packet_size=view.packet_size,
        )

    @inject
    async def ReadIPInfo(  # noqa: N802
        self,
        request: internet_protocol_pb2.ReadIPInfoRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadIPInfoQueryHandler],
    ) -> internet_protocol_pb2.ReadIPInfoResponse:
        query = ReadIPInfoQuery(ip_address=request.ip_address)
        view = await handler(query)
        return internet_protocol_pb2.ReadIPInfoResponse(
            ip_address=view.ip_address,
            isp=view.isp,
            organization=view.organization,
            country=view.country,
            region_name=view.region_name,
            city=view.city,
            zip_code=view.zip_code,
            latitude=view.latitude,
            longitude=view.longitude,
            has_location=view.has_location,
            has_network_info=view.has_network_info,
            location_string=view.location_string,
            network_string=view.network_string,
        )

    @inject
    async def ScanPort(  # noqa: N802
        self,
        request: internet_protocol_pb2.ScanPortRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ScanPortQueryHandler],
    ) -> internet_protocol_pb2.PortScanResultResponse:
        query = ScanPortQuery(
            target=request.target,
            port=request.port,
            timeout=request.timeout or 1.0,
        )
        view = await handler(query)
        return _port_scan_view_to_proto(view)

    @inject
    async def ScanPorts(  # noqa: N802
        self,
        request: internet_protocol_pb2.ScanPortsRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ScanPortsQueryHandler],
    ) -> internet_protocol_pb2.ScanPortsResponse:
        query = ScanPortsQuery(
            target=request.target,
            ports=list(request.ports),
            timeout=request.timeout or 1.0,
            max_concurrent=request.max_concurrent or 100,
        )
        views = await handler(query)
        return internet_protocol_pb2.ScanPortsResponse(
            results=[_port_scan_view_to_proto(v) for v in views],
        )

    @inject
    async def ScanPortRange(  # noqa: N802
        self,
        request: internet_protocol_pb2.ScanPortRangeRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ScanPortRangeQueryHandler],
    ) -> internet_protocol_pb2.PortScanSummaryResponse:
        query = ScanPortRangeQuery(
            target=request.target,
            start_port=request.start_port,
            end_port=request.end_port,
            timeout=request.timeout or 1.0,
            max_concurrent=request.max_concurrent or 100,
        )
        view = await handler(query)
        return self._summary_view_to_proto(view)

    @inject
    async def ScanCommonPorts(  # noqa: N802
        self,
        request: internet_protocol_pb2.ScanCommonPortsRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ScanCommonPortsQueryHandler],
    ) -> internet_protocol_pb2.PortScanSummaryResponse:
        query = ScanCommonPortsQuery(
            target=request.target,
            timeout=request.timeout or 1.0,
            max_concurrent=request.max_concurrent or 100,
        )
        view = await handler(query)
        return self._summary_view_to_proto(view)

    @inject
    async def AnalyzeDomain(  # noqa: N802
        self,
        request: internet_protocol_pb2.AnalyzeDomainRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[AnalyzeDomainQueryHandler],
    ) -> internet_protocol_pb2.AnalyzeDomainResponse:
        query = AnalyzeDomainQuery(
            domain=request.domain,
            timeout=request.timeout or 10.0,
        )
        view = await handler(query)
        dns_records = []
        if view.dns_records:
            dns_records = [
                internet_protocol_pb2.DnsRecordEntry(record_type=rtype, values=values)
                for rtype, values in view.dns_records.items()
            ]
        return internet_protocol_pb2.AnalyzeDomainResponse(
            domain_id=str(view.domain_id),
            domain_name=view.domain_name,
            dns_records=dns_records,
            subdomains=view.subdomains,
            title=view.title,
            created_at=view.created_at.isoformat() if view.created_at else None,
            updated_at=view.updated_at.isoformat() if view.updated_at else None,
        )

    @staticmethod
    def _summary_view_to_proto(
        view: object,
    ) -> internet_protocol_pb2.PortScanSummaryResponse:
        results = [
            internet_protocol_pb2.PortScanResultResponse(
                port=r.get("port", 0),
                status=r.get("status", ""),
                response_time=r.get("response_time"),
                service=r.get("service"),
                error_message=r.get("error_message"),
                scanned_at=r.get("scanned_at"),
            )
            for r in view.results  # type: ignore[attr-defined]
        ]
        return internet_protocol_pb2.PortScanSummaryResponse(
            target=view.target,  # type: ignore[attr-defined]
            port_range=view.port_range,  # type: ignore[attr-defined]
            total_ports=view.total_ports,  # type: ignore[attr-defined]
            open_ports=view.open_ports,  # type: ignore[attr-defined]
            closed_ports=view.closed_ports,  # type: ignore[attr-defined]
            filtered_ports=view.filtered_ports,  # type: ignore[attr-defined]
            scan_duration=view.scan_duration,  # type: ignore[attr-defined]
            started_at=view.started_at.isoformat(),  # type: ignore[attr-defined]
            completed_at=view.completed_at.isoformat(),  # type: ignore[attr-defined]
            success_rate=view.success_rate,  # type: ignore[attr-defined]
            results=results,
        )
