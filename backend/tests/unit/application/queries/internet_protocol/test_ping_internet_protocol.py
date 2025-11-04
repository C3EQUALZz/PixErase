from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.ping_internet_protocol import (
    PingInternetProtocolView,
)
from pix_erase.application.queries.internet_protocol.ping_internet_protocol import (
    PingInternetProtocolQuery,
    PingInternetProtocolQueryHandler,
)
from pix_erase.domain.internet_protocol.services.internet_protocol_service import (
    InternetProtocolService,
)
from pix_erase.domain.internet_protocol.values import PingResult
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address


@pytest.mark.asyncio
async def test_ping_internet_protocol_success(
    fake_current_user_service: CurrentUserService,
    fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    fake_internet_service.create.return_value = IPv4Address(value="8.8.8.8")  # type: ignore[assignment]
    fake_internet_service.ping = AsyncMock(
        return_value=PingResult(success=True, response_time_ms=12.5, ttl=20, packet_size=56)
    )

    sut = PingInternetProtocolQueryHandler(
        ping_service=fake_internet_service,
        current_user_service=fake_current_user_service,
    )

    query = PingInternetProtocolQuery(destination_address="8.8.8.8", timeout=4.0, packet_size=56, ttl=20)

    # Act
    view: PingInternetProtocolView = await sut(query)

    # Assert
    assert view.success is True
    assert view.response_time_ms == 12.5
    assert view.ttl == 20
    assert view.packet_size == 56

