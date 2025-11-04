from datetime import UTC, datetime

import pytest

from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidIPAddressError
from pix_erase.domain.internet_protocol.ports.ip_info_service_port import IPInfoServicePort
from pix_erase.domain.internet_protocol.ports.ping_service_port import PingServicePort
from pix_erase.domain.internet_protocol.ports.port_scan_service_port import PortScanServicePort
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import (
    PortScanResult,
    PortScanSummary,
    PortStatus,
)
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPInfo
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress, IPv4Address, IPv6Address
from pix_erase.domain.internet_protocol.values.port import PortRange
from tests.unit.factories.value_objects import (
    create_ipv4_address,
    create_ipv6_address,
    create_packet_size,
    create_ping_result,
    create_port,
    create_time_to_live,
    create_timeout,
)


@pytest.mark.parametrize(
    ("address", "expected_type"),
    [
        pytest.param("192.168.1.1", IPv4Address, id="ipv4"),
        pytest.param("8.8.8.8", IPv4Address, id="public_ipv4"),
        pytest.param("2001:db8::1", IPv6Address, id="ipv6"),
    ],
)
def test_create_returns_correct_ip_address_type(
    address: str,
    expected_type: type[IPAddress],
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    # Act
    result = sut.create(address)

    # Assert
    assert isinstance(result, expected_type)
    assert result.value == address


def test_create_rejects_invalid_address(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    # Act & Assert
    with pytest.raises(InvalidIPAddressError):
        sut.create("invalid_address")


@pytest.mark.asyncio
async def test_ping_calls_service_with_correct_parameters(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    expected_result = create_ping_result()
    ping_service.ping.return_value = expected_result

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    destination = create_ipv4_address()
    timeout = create_timeout(5.0)
    packet_size = create_packet_size(64)
    ttl = create_time_to_live(128)

    # Act
    result = await sut.ping(destination, timeout, packet_size, ttl)

    # Assert
    assert result == expected_result
    ping_service.ping.assert_called_once_with(
        destination=destination,
        timeout=5.0,
        packet_size=64,
        ttl=128,
    )


@pytest.mark.asyncio
async def test_ping_without_ttl(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    expected_result = create_ping_result()
    ping_service.ping.return_value = expected_result

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    destination = create_ipv4_address()
    timeout = create_timeout()
    packet_size = create_packet_size()

    # Act
    result = await sut.ping(destination, timeout, packet_size)

    # Assert
    assert result == expected_result
    ping_service.ping.assert_called_once_with(
        destination=destination,
        timeout=4.0,
        packet_size=56,
        ttl=None,
    )


@pytest.mark.asyncio
async def test_ping_multiple_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    expected_results = [create_ping_result(), create_ping_result()]
    ping_service.ping_multiple.return_value = expected_results

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    destinations = [create_ipv4_address(), create_ipv6_address()]
    timeout = create_timeout()
    packet_size = create_packet_size()

    # Act
    result = await sut.ping_multiple(destinations, timeout, packet_size)

    # Assert
    assert result == expected_results
    ping_service.ping_multiple.assert_called_once_with(
        destinations=destinations,
        timeout=4.0,
        packet_size=56,
        ttl=None,
    )


@pytest.mark.asyncio
async def test_get_ip_info_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange

    expected_info = IPInfo(ip_address="192.168.1.1")
    ip_info_service.get_ip_info.return_value = expected_info

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    ip_address = create_ipv4_address()

    # Act
    result = await sut.get_ip_info(ip_address)

    # Assert
    assert result == expected_info
    ip_info_service.get_ip_info.assert_called_once_with(ip_address)


@pytest.mark.asyncio
async def test_scan_port_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange
    expected_result = PortScanResult(
        port=create_port(),
        status=PortStatus.CLOSED,
        response_time=None,
    )
    port_scan_service.scan_port.return_value = expected_result

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    target = create_ipv4_address()
    port = create_port(80)
    timeout = create_timeout()

    # Act
    result = await sut.scan_port(target, port, timeout)

    # Assert
    assert result == expected_result
    port_scan_service.scan_port.assert_called_once_with(
        target=target,
        port=port,
        timeout=4.0,
    )


@pytest.mark.asyncio
async def test_scan_ports_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange

    expected_results = [
        PortScanResult(port=create_port(80), status=PortStatus.OPEN, response_time=10.0),
        PortScanResult(port=create_port(443), status=PortStatus.CLOSED, response_time=None),
    ]
    port_scan_service.scan_ports.return_value = expected_results

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    target = create_ipv4_address()
    ports = [create_port(80), create_port(443)]
    timeout = create_timeout()

    # Act
    result = await sut.scan_ports(target, ports, timeout)

    # Assert
    assert result == expected_results
    port_scan_service.scan_ports.assert_called_once_with(
        target=target,
        ports=ports,
        timeout=4.0,
        max_concurrent=100,
    )


@pytest.mark.asyncio
async def test_scan_port_range_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange

    expected_summary = PortScanSummary(
        target="192.168.1.1",
        port_range="80-179",
        total_ports=100,
        open_ports=0,
        closed_ports=0,
        filtered_ports=0,
        scan_duration=10.0,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        results=[],
    )
    port_scan_service.scan_port_range.return_value = expected_summary

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    target = create_ipv4_address()
    port_range = PortRange(start=create_port(80), end=create_port(179))
    timeout = create_timeout()

    # Act
    result = await sut.scan_port_range(target, port_range, timeout)

    # Assert
    assert result == expected_summary
    port_scan_service.scan_port_range.assert_called_once_with(
        target=target,
        port_range=port_range,
        timeout=4.0,
        max_concurrent=100,
    )


@pytest.mark.asyncio
async def test_scan_common_ports_calls_service(
    ping_service: PingServicePort,
    ip_info_service: IPInfoServicePort,
    port_scan_service: PortScanServicePort,
) -> None:
    # Arrange

    expected_summary = PortScanSummary(
        target="192.168.1.1",
        port_range="1-1023",
        total_ports=1023,
        open_ports=0,
        closed_ports=0,
        filtered_ports=0,
        scan_duration=100.0,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        results=[],
    )
    port_scan_service.scan_common_ports.return_value = expected_summary

    sut = InternetProtocolService(
        ping_service=ping_service,
        ip_info_service=ip_info_service,
        port_scan_service=port_scan_service,
    )

    target = create_ipv4_address()
    timeout = create_timeout()

    # Act
    result = await sut.scan_common_ports(target, timeout)

    # Assert
    assert result == expected_summary
    port_scan_service.scan_common_ports.assert_called_once_with(
        target=target,
        timeout=4.0,
        max_concurrent=100,
    )
