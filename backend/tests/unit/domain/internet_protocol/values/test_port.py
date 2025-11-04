# ruff: noqa: PLR2004

import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadPortError, BadPortRangeError
from pix_erase.domain.internet_protocol.values.port import (
    ALL_PORTS,
    COMMON_PORTS,
    DYNAMIC_PORTS,
    REGISTERED_PORTS,
    Port,
    PortRange,
)
from tests.unit.factories.value_objects import create_port


@pytest.mark.parametrize(
    "port_value",
    [
        pytest.param(1, id="min_port"),
        pytest.param(80, id="http_port"),
        pytest.param(443, id="https_port"),
        pytest.param(1023, id="max_well_known"),
        pytest.param(1024, id="min_registered"),
        pytest.param(49151, id="max_registered"),
        pytest.param(49152, id="min_dynamic"),
        pytest.param(65535, id="max_port"),
    ],
)
def test_accepts_valid_port(port_value: int) -> None:
    # Arrange & Act
    sut = Port(value=port_value)

    # Assert
    assert sut.value == port_value
    assert str(sut) == str(port_value)


@pytest.mark.parametrize(
    ("port_value", "expected_error"),
    [
        pytest.param(0, BadPortError, id="below_min"),
        pytest.param(65536, BadPortError, id="above_max"),
        pytest.param(-1, BadPortError, id="negative"),
    ],
)
def test_rejects_invalid_port(port_value: int, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        Port(value=port_value)


@pytest.mark.parametrize(
    ("port_value", "expected"),
    [
        pytest.param(80, True, id="well_known"),
        pytest.param(443, True, id="well_known_https"),
        pytest.param(1024, False, id="registered"),
        pytest.param(49152, False, id="dynamic"),
    ],
)
def test_is_well_known_property(port_value: int, expected: bool) -> None:
    # Arrange
    sut = create_port(port_value)

    # Act
    result = sut.is_well_known

    # Assert
    assert result is expected


@pytest.mark.parametrize(
    ("port_value", "expected"),
    [
        pytest.param(1024, True, id="registered"),
        pytest.param(49151, True, id="max_registered"),
        pytest.param(80, False, id="well_known"),
        pytest.param(49152, False, id="dynamic"),
    ],
)
def test_is_registered_property(port_value: int, expected: bool) -> None:
    # Arrange
    sut = create_port(port_value)

    # Act
    result = sut.is_registered

    # Assert
    assert result is expected


@pytest.mark.parametrize(
    ("port_value", "expected"),
    [
        pytest.param(49152, True, id="dynamic"),
        pytest.param(65535, True, id="max_dynamic"),
        pytest.param(80, False, id="well_known"),
        pytest.param(1024, False, id="registered"),
    ],
)
def test_is_dynamic_property(port_value: int, expected: bool) -> None:
    # Arrange
    sut = create_port(port_value)

    # Act
    result = sut.is_dynamic

    # Assert
    assert result is expected


@pytest.mark.parametrize(
    ("port_value", "expected_category"),
    [
        pytest.param(80, "well-known", id="well_known"),
        pytest.param(1024, "registered", id="registered"),
        pytest.param(49152, "dynamic", id="dynamic"),
    ],
)
def test_category_property(port_value: int, expected_category: str) -> None:
    # Arrange
    sut = create_port(port_value)

    # Act
    result = sut.category

    # Assert
    assert result == expected_category


def test_port_equality() -> None:
    # Arrange
    port_value = 80
    port1 = Port(value=port_value)
    port2 = Port(value=port_value)

    # Assert
    assert port1 == port2
    assert hash(port1) == hash(port2)


def test_port_inequality() -> None:
    # Arrange
    port1 = create_port(80)
    port2 = create_port(443)

    # Assert
    assert port1 != port2


def test_port_range_accepts_valid_range() -> None:
    # Arrange & Act
    sut = PortRange(start=Port(value=80), end=Port(value=443))

    # Assert
    assert sut.start.value == 80
    assert sut.end.value == 443
    assert str(sut) == "80-443"


def test_port_range_rejects_invalid_range() -> None:
    # Arrange & Act & Assert
    with pytest.raises(BadPortRangeError):
        PortRange(start=Port(value=443), end=Port(value=80))


def test_port_range_count() -> None:
    # Arrange
    sut = PortRange(start=Port(value=80), end=Port(value=82))

    # Act
    result = sut.count

    # Assert
    assert result == 3


def test_port_range_iteration() -> None:
    # Arrange
    sut = PortRange(start=Port(value=80), end=Port(value=82))

    # Act
    ports = list(sut)

    # Assert
    assert len(ports) == 3
    assert ports[0].value == 80
    assert ports[1].value == 81
    assert ports[2].value == 82


def test_common_ports_constant() -> None:
    # Arrange & Act
    sut = COMMON_PORTS

    # Assert
    assert sut.start.value == 1
    assert sut.end.value == 1023


def test_registered_ports_constant() -> None:
    # Arrange & Act
    sut = REGISTERED_PORTS

    # Assert
    assert sut.start.value == 1024
    assert sut.end.value == 49151


def test_dynamic_ports_constant() -> None:
    # Arrange & Act
    sut = DYNAMIC_PORTS

    # Assert
    assert sut.start.value == 49152
    assert sut.end.value == 65535


def test_all_ports_constant() -> None:
    # Arrange & Act
    sut = ALL_PORTS

    # Assert
    assert sut.start.value == 1
    assert sut.end.value == 65535
