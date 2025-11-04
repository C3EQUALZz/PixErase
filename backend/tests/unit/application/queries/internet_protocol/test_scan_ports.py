from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanView
from pix_erase.application.queries.internet_protocol.scan_ports import (
    ScanPortsQuery,
    ScanPortsQueryHandler,
)
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import (
    PortScanResult,
    PortStatus,
)
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address
from pix_erase.domain.internet_protocol.values.port import Port


@pytest.mark.asyncio
async def test_scan_ports_success(
    fake_current_user_service: CurrentUserService,
    fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    fake_internet_service.create.return_value = IPv4Address(value="192.168.0.1")  # type: ignore[assignment]
    now = datetime.now(UTC)
    fake_internet_service.scan_ports = AsyncMock(
        return_value=[
            PortScanResult(port=Port(22), status=PortStatus.CLOSED, response_time=0.02, scanned_at=now),
            PortScanResult(port=Port(443), status=PortStatus.OPEN, response_time=0.03, service="https", scanned_at=now),
        ]
    )

    sut = ScanPortsQueryHandler(
        internet_protocol_service=fake_internet_service,
        current_user_service=fake_current_user_service,
    )

    query = ScanPortsQuery(target="192.168.0.1", ports=[22, 443], timeout=1.5, max_concurrent=50)

    # Act
    views: list[PortScanView] = await sut(query)

    # Assert
    assert len(views) == 2
    assert views[0].port == 22 and views[0].status == PortStatus.CLOSED.value
    assert views[1].port == 443 and views[1].status == PortStatus.OPEN.value and views[1].service == "https"

