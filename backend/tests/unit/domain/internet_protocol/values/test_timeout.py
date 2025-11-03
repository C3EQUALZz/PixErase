import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadTimeOutError
from pix_erase.domain.internet_protocol.values.timeout import Timeout
from tests.unit.factories.value_objects import create_timeout


@pytest.mark.parametrize(
    "timeout_value",
    [
        pytest.param(0.1, id="small"),
        pytest.param(1.0, id="one_second"),
        pytest.param(4.0, id="default"),
        pytest.param(60.0, id="one_minute"),
        pytest.param(300.0, id="max_timeout"),
    ],
)
def test_accepts_valid_timeout(timeout_value: float) -> None:
    # Arrange & Act
    sut = Timeout(value=timeout_value)

    # Assert
    assert sut.value == timeout_value
    assert str(sut) == f"{timeout_value} s"


@pytest.mark.parametrize(
    ("timeout_value", "expected_error"),
    [
        pytest.param(0.0, BadTimeOutError, id="zero"),
        pytest.param(-1.0, BadTimeOutError, id="negative"),
        pytest.param(300.1, BadTimeOutError, id="above_max"),
        pytest.param(1000.0, BadTimeOutError, id="way_above_max"),
    ],
)
def test_rejects_invalid_timeout(timeout_value: float, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        Timeout(value=timeout_value)


def test_timeout_equality() -> None:
    # Arrange
    timeout_value = 4.0
    timeout1 = Timeout(value=timeout_value)
    timeout2 = Timeout(value=timeout_value)

    # Assert
    assert timeout1 == timeout2
    assert hash(timeout1) == hash(timeout2)


def test_timeout_inequality() -> None:
    # Arrange
    timeout1 = create_timeout(4.0)
    timeout2 = create_timeout(5.0)

    # Assert
    assert timeout1 != timeout2


