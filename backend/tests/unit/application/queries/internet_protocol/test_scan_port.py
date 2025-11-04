from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanView
from pix_erase.application.queries.internet_protocol.scan_port import (
    ScanPortQuery,
    ScanPortQueryHandler,
)
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import (
    PortScanResult,
    PortStatus,
)
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address
from pix_erase.domain.internet_protocol.values.port import Port


@pytest.mark.asyncio
async def test_scan_port_success(
    fake_current_user_service: CurrentUserService,
    fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    fake_internet_service.create.return_value = IPv4Address(value="127.0.0.1")  # type: ignore[assignment]
    now = datetime.now(UTC)
    fake_internet_service.scan_port = AsyncMock(
        return_value=PortScanResult(
            port=Port(80),
            status=PortStatus.OPEN,
            response_time=0.01,
            service="http",
            scanned_at=now,
        )
    )

    sut = ScanPortQueryHandler(
        internet_protocol_service=fake_internet_service,
        current_user_service=fake_current_user_service,
    )

    query = ScanPortQuery(target="127.0.0.1", port=80, timeout=1.0)

    # Act
    view: PortScanView = await sut(query)

    # Assert
    assert view.port == 80
    assert view.status == PortStatus.OPEN.value
    assert view.response_time == 0.01
    assert view.service == "http"
    assert view.scanned_at == now

