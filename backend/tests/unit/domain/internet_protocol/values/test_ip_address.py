# ruff: noqa: PLR2004

import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidIPAddressError
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address, IPv6Address
from tests.unit.factories.value_objects import create_ipv4_address


@pytest.mark.parametrize(
    "address",
    [
        pytest.param("192.168.1.1", id="private_ipv4"),
        pytest.param("8.8.8.8", id="public_ipv4"),
        pytest.param("127.0.0.1", id="loopback_ipv4"),
        pytest.param("10.0.0.1", id="private_range_a"),
        pytest.param("172.16.0.1", id="private_range_b"),
    ],
)
def test_accepts_valid_ipv4_address(address: str) -> None:
    # Arrange & Act
    sut = IPv4Address(value=address)

    # Assert
    assert sut.value == address
    assert sut.version == 4
    assert str(sut) == address


@pytest.mark.parametrize(
    "address",
    [
        pytest.param("2001:0db8:85a3:0000:0000:8a2e:0370:7334", id="full_ipv6"),
        pytest.param("2001:db8:85a3::8a2e:370:7334", id="compressed_ipv6"),
        pytest.param("::1", id="loopback_ipv6"),
        pytest.param("fe80::1", id="link_local_ipv6"),
        pytest.param("2001:db8::1", id="short_ipv6"),
    ],
)
def test_accepts_valid_ipv6_address(address: str) -> None:
    # Arrange & Act
    sut = IPv6Address(value=address)

    # Assert
    assert sut.value == address
    assert sut.version == 6
    assert str(sut) == address


@pytest.mark.parametrize(
    ("address", "expected_error"),
    [
        pytest.param("", InvalidIPAddressError, id="empty"),
        pytest.param("invalid", InvalidIPAddressError, id="invalid_string"),
        pytest.param("256.1.1.1", InvalidIPAddressError, id="out_of_range"),
        pytest.param("192.168.1", InvalidIPAddressError, id="incomplete_ipv4"),
        pytest.param("192.168.1.1.1", InvalidIPAddressError, id="too_many_octets"),
        pytest.param("::ffff:192.168.1.1", InvalidIPAddressError, id="ipv6_mapped_in_ipv4"),
    ],
)
def test_ipv4_rejects_invalid_address(address: str, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        IPv4Address(value=address)


@pytest.mark.parametrize(
    ("address", "expected_error"),
    [
        pytest.param("192.168.1.1", InvalidIPAddressError, id="ipv4_in_ipv6"),
        pytest.param("invalid", InvalidIPAddressError, id="invalid_string"),
        pytest.param("2001:db8::1::1", InvalidIPAddressError, id="double_colon"),
        pytest.param("2001:db8:z::1", InvalidIPAddressError, id="invalid_char"),
    ],
)
def test_ipv6_rejects_invalid_address(address: str, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        IPv6Address(value=address)


@pytest.mark.parametrize(
    ("address", "expected"),
    [
        pytest.param("192.168.1.1", True, id="private_ipv4"),
        pytest.param("10.0.0.1", True, id="private_range"),
        pytest.param("8.8.8.8", False, id="public_ipv4"),
        pytest.param("127.0.0.1", True, id="loopback_is_private"),
    ],
)
def test_is_private_property(address: str, expected: bool) -> None:
    # Arrange
    sut = IPv4Address(value=address)

    # Act
    result = sut.is_private

    # Assert
    assert result is expected


def test_is_loopback_property() -> None:
    # Arrange
    sut = IPv4Address(value="127.0.0.1")

    # Act
    result = sut.is_loopback

    # Assert
    assert result is True


def test_is_multicast_property() -> None:
    # Arrange
    sut = IPv4Address(value="224.0.0.1")

    # Act
    result = sut.is_multicast

    # Assert
    assert result is True


def test_is_reserved_property() -> None:
    # Arrange
    sut = IPv4Address(value="240.0.0.1")

    # Act
    result = sut.is_reserved

    # Assert
    assert result is True


def test_ipv4_equality() -> None:
    # Arrange
    address = "192.168.1.1"
    ip1 = IPv4Address(value=address)
    ip2 = IPv4Address(value=address)

    # Assert
    assert ip1 == ip2
    assert hash(ip1) == hash(ip2)


def test_ipv6_equality() -> None:
    # Arrange
    address = "2001:db8::1"
    ip1 = IPv6Address(value=address)
    ip2 = IPv6Address(value=address)

    # Assert
    assert ip1 == ip2
    assert hash(ip1) == hash(ip2)


def test_ipv4_inequality() -> None:
    # Arrange
    ip1 = create_ipv4_address("192.168.1.1")
    ip2 = create_ipv4_address("192.168.1.2")

    # Assert
    assert ip1 != ip2
