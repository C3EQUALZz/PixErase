from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanSummaryView
from pix_erase.application.queries.internet_protocol.scan_port_range import (
    ScanPortRangeQuery,
    ScanPortRangeQueryHandler,
)
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import (
    PortScanResult,
    PortScanSummary,
    PortStatus,
)
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address
from pix_erase.domain.internet_protocol.values.port import Port


@pytest.mark.asyncio
async def test_scan_port_range_success(
    fake_current_user_service: CurrentUserService,
    fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    fake_internet_service.create.return_value = IPv4Address(value="10.0.0.1")  # type: ignore[assignment]
    now = datetime.now(UTC)
    results = [
        PortScanResult(port=Port(80), status=PortStatus.OPEN, response_time=0.01, service="http", scanned_at=now),
        PortScanResult(port=Port(81), status=PortStatus.CLOSED, response_time=0.02, scanned_at=now),
    ]
    summary = PortScanSummary(
        target="10.0.0.1",
        port_range="80-81",
        total_ports=2,
        open_ports=1,
        closed_ports=1,
        filtered_ports=0,
        scan_duration=0.05,
        started_at=now,
        completed_at=now,
        results=results,
    )
    fake_internet_service.scan_port_range = AsyncMock(return_value=summary)

    sut = ScanPortRangeQueryHandler(
        internet_protocol_service=fake_internet_service,
        current_user_service=fake_current_user_service,
    )

    query = ScanPortRangeQuery(target="10.0.0.1", start_port=80, end_port=81, timeout=1.0, max_concurrent=10)

    # Act
    view: PortScanSummaryView = await sut(query)

    # Assert
    assert view.target == summary.target
    assert view.port_range == summary.port_range
    assert view.total_ports == 2
    assert view.open_ports == 1
    assert view.closed_ports == 1
    assert view.filtered_ports == 0
    assert len(view.results) == 2

