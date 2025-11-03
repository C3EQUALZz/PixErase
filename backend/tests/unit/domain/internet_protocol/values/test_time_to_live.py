import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadTimeToLiveError
from pix_erase.domain.internet_protocol.values.time_to_live import TimeToLive
from tests.unit.factories.value_objects import create_time_to_live


@pytest.mark.parametrize(
    "ttl_value",
    [
        pytest.param(1, id="min_ttl"),
        pytest.param(64, id="default"),
        pytest.param(128, id="common"),
        pytest.param(255, id="max_ttl"),
    ],
)
def test_accepts_valid_ttl(ttl_value: int) -> None:
    # Arrange & Act
    sut = TimeToLive(value=ttl_value)

    # Assert
    assert sut.value == ttl_value
    assert str(sut) == f"{ttl_value} s"


@pytest.mark.parametrize(
    ("ttl_value", "expected_error"),
    [
        pytest.param(0, BadTimeToLiveError, id="zero"),
        pytest.param(-1, BadTimeToLiveError, id="negative"),
        pytest.param(256, BadTimeToLiveError, id="above_max"),
        pytest.param(1000, BadTimeToLiveError, id="way_above_max"),
    ],
)
def test_rejects_invalid_ttl(ttl_value: int, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        TimeToLive(value=ttl_value)


def test_ttl_equality() -> None:
    # Arrange
    ttl_value = 64
    ttl1 = TimeToLive(value=ttl_value)
    ttl2 = TimeToLive(value=ttl_value)

    # Assert
    assert ttl1 == ttl2
    assert hash(ttl1) == hash(ttl2)


def test_ttl_inequality() -> None:
    # Arrange
    ttl1 = create_time_to_live(64)
    ttl2 = create_time_to_live(128)

    # Assert
    assert ttl1 != ttl2


