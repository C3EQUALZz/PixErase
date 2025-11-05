import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadPackageSizeError
from pix_erase.domain.internet_protocol.values.packet_size import PacketSize
from tests.unit.factories.value_objects import create_packet_size


@pytest.mark.parametrize(
    "packet_size_value",
    [
        pytest.param(8, id="min_size"),
        pytest.param(56, id="default"),
        pytest.param(64, id="small"),
        pytest.param(512, id="medium"),
        pytest.param(1500, id="max_size"),
    ],
)
def test_accepts_valid_packet_size(packet_size_value: int) -> None:
    # Arrange & Act
    sut = PacketSize(value=packet_size_value)

    # Assert
    assert sut.value == packet_size_value
    assert str(sut) == f"{packet_size_value} bytes"


@pytest.mark.parametrize(
    ("packet_size_value", "expected_error"),
    [
        pytest.param(7, BadPackageSizeError, id="below_min"),
        pytest.param(0, BadPackageSizeError, id="zero"),
        pytest.param(-1, BadPackageSizeError, id="negative"),
        pytest.param(1501, BadPackageSizeError, id="above_max"),
        pytest.param(2000, BadPackageSizeError, id="way_above_max"),
    ],
)
def test_rejects_invalid_packet_size(
    packet_size_value: int,
    expected_error: type[DomainFieldError],
) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        PacketSize(value=packet_size_value)


def test_packet_size_equality() -> None:
    # Arrange
    packet_size_value = 56
    packet_size1 = PacketSize(value=packet_size_value)
    packet_size2 = PacketSize(value=packet_size_value)

    # Assert
    assert packet_size1 == packet_size2
    assert hash(packet_size1) == hash(packet_size2)


def test_packet_size_inequality() -> None:
    # Arrange
    packet_size1 = create_packet_size(56)
    packet_size2 = create_packet_size(64)

    # Assert
    assert packet_size1 != packet_size2
