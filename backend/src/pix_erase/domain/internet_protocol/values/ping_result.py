from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidPingResultError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class PingResult(BaseValueObject):
    """
    Value object representing the result of a ping operation.

    This encapsulates all the information returned from a ping operation,
    including success status, response time, and any error information.
    """

    success: bool
    response_time_ms: float | None = None
    error_message: str | None = None
    ttl: int | None = None
    packet_size: int | None = None

    @override
    def _validate(self) -> None:
        """Validate the ping result data."""
        if not self.success and self.response_time_ms is not None:
            msg = "Cannot have response time for failed ping"
            raise InvalidPingResultError(msg)

        if self.success and self.response_time_ms is None:
            msg = "Successful ping must have response time"
            raise InvalidPingResultError(msg)

        if self.response_time_ms is not None and self.response_time_ms < 0:
            msg = "Response time cannot be negative"
            raise InvalidPingResultError(msg)

        if self.ttl is not None and self.ttl < 0:
            msg = "TTL cannot be negative"
            raise InvalidPingResultError(msg)

        if self.packet_size is not None and self.packet_size < 0:
            msg = "Packet size cannot be negative"
            raise InvalidPingResultError(msg)

    @override
    def __str__(self) -> str:
        if self.success:
            return f"Ping successful: {self.response_time_ms:.2f}ms"
        return f"Ping failed: {self.error_message or 'Unknown error'}"
