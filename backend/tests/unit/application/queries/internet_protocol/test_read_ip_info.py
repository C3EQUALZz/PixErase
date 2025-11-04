from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.ip_info import IPInfoView
from pix_erase.application.queries.internet_protocol.read_ip_info import (
    ReadIPInfoQuery,
    ReadIPInfoQueryHandler,
)
from pix_erase.domain.internet_protocol.errors import PingDestinationUnreachableError
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPInfo, PingResult
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address


@pytest.mark.asyncio
async def test_read_ip_info_success(
        fake_current_user_service: CurrentUserService,
        fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    ip_address = IPv4Address(value="8.8.8.8")
    fake_internet_service.create.return_value = ip_address  # type: ignore[assignment]
    fake_internet_service.ping = AsyncMock(
        return_value=PingResult(success=True, response_time_ms=10.0)
    )
    ip_info = IPInfo(
        ip_address="8.8.8.8",
        isp="ISP",
        organization="Org",
        country="US",
        region_name="CA",
        city="Mountain View",
        zip_code="94043",
        latitude=37.0,
        longitude=-122.0,
    )
    fake_internet_service.get_ip_info = AsyncMock(return_value=ip_info)  # type: ignore[attr-defined]

    sut = ReadIPInfoQueryHandler(internet_service=fake_internet_service, current_user_service=fake_current_user_service)
    query = ReadIPInfoQuery(ip_address="8.8.8.8")

    # Act
    view: IPInfoView = await sut(query)

    # Assert
    assert view.ip_address == ip_info.ip_address
    assert view.isp == ip_info.isp
    assert view.organization == ip_info.organization
    assert view.country == ip_info.country
    assert view.region_name == ip_info.region_name
    assert view.city == ip_info.city
    assert view.zip_code == ip_info.zip_code
    assert view.latitude == ip_info.latitude
    assert view.longitude == ip_info.longitude
    assert view.has_location is True
    assert view.has_network_info is True
    assert view.location_string != ""
    assert view.network_string != ""


@pytest.mark.asyncio
async def test_read_ip_info_raises_when_ping_failed(
        fake_current_user_service: CurrentUserService,
        fake_internet_service: InternetProtocolService,
) -> None:
    # Arrange
    ip_address = IPv4Address(value="1.1.1.1")
    fake_internet_service.create.return_value = ip_address  # type: ignore[assignment]
    # Failed ping
    fake_internet_service.ping = AsyncMock(
        return_value=PingResult(success=False, error_message="timeout"),  # type: ignore[arg-type]
    )

    sut = ReadIPInfoQueryHandler(
        internet_service=fake_internet_service,
        current_user_service=fake_current_user_service
    )
    query = ReadIPInfoQuery(ip_address="1.1.1.1")

    # Act / Assert
    with pytest.raises(PingDestinationUnreachableError):
        await sut(query)
