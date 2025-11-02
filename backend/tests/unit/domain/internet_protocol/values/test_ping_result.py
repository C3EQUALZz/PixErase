import pytest

from pix_erase.domain.common.errors.base import DomainError
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidPingResultError
from pix_erase.domain.internet_protocol.values.ping_result import PingResult
from tests.unit.factories.value_objects import create_ping_result


def test_accepts_valid_successful_ping() -> None:
    # Arrange & Act
    sut = PingResult(
        success=True,
        response_time_ms=10.5,
        ttl=64,
        packet_size=56,
    )

    # Assert
    assert sut.success is True
    assert sut.response_time_ms == 10.5
    assert sut.ttl == 64
    assert sut.packet_size == 56
    assert "successful" in str(sut).lower()


def test_accepts_valid_failed_ping() -> None:
    # Arrange & Act
    sut = PingResult(
        success=False,
        error_message="Destination unreachable",
    )

    # Assert
    assert sut.success is False
    assert sut.error_message == "Destination unreachable"
    assert sut.response_time_ms is None
    assert "failed" in str(sut).lower()


@pytest.mark.parametrize(
    ("success", "response_time_ms", "error_message", "expected_error"),
    [
        pytest.param(False, 10.5, None, InvalidPingResultError, id="failed_with_response_time"),
        pytest.param(True, None, None, InvalidPingResultError, id="success_without_response_time"),
        pytest.param(True, -1.0, None, InvalidPingResultError, id="negative_response_time"),
        pytest.param(True, 10.5, None, InvalidPingResultError, id="negative_ttl"),
    ],
)
def test_rejects_invalid_ping_result(
    success: bool,
    response_time_ms: float | None,
    error_message: str | None,
    expected_error: type[DomainError],
) -> None:
    # Arrange
    ttl = -1 if success else None

    # Act & Assert
    with pytest.raises(expected_error):
        PingResult(
            success=success,
            response_time_ms=response_time_ms,
            error_message=error_message,
            ttl=ttl,
        )


def test_rejects_negative_packet_size() -> None:
    # Arrange & Act & Assert
    with pytest.raises(InvalidPingResultError):
        PingResult(
            success=True,
            response_time_ms=10.5,
            packet_size=-1,
        )


def test_ping_result_equality() -> None:
    # Arrange
    ping_result1 = create_ping_result(success=True, response_time_ms=10.5)
    ping_result2 = create_ping_result(success=True, response_time_ms=10.5)

    # Assert
    assert ping_result1 == ping_result2
    assert hash(ping_result1) == hash(ping_result2)


def test_ping_result_inequality() -> None:
    # Arrange
    ping_result1 = create_ping_result(success=True, response_time_ms=10.5)
    ping_result2 = create_ping_result(success=True, response_time_ms=20.0)

    # Assert
    assert ping_result1 != ping_result2


def test_ping_result_str_successful() -> None:
    # Arrange
    sut = create_ping_result(success=True, response_time_ms=10.5)

    # Act
    result = str(sut)

    # Assert
    assert "successful" in result.lower()
    assert "10.5" in result


def test_ping_result_str_failed() -> None:
    # Arrange
    sut = create_ping_result(success=False, error_message="Timeout")

    # Act
    result = str(sut)

    # Assert
    assert "failed" in result.lower()
    assert "Timeout" in result

