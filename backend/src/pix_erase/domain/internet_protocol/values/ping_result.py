from dataclasses import dataclass
from typing import Optional, override

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
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    ttl: Optional[int] = None
    packet_size: Optional[int] = None
    
    @override
    def _validate(self) -> None:
        """Validate the ping result data."""
        if not self.success and self.response_time_ms is not None:
            raise InvalidPingResultError(
                "Cannot have response time for failed ping"
            )
        
        if self.success and self.response_time_ms is None:
            raise InvalidPingResultError(
                "Successful ping must have response time"
            )
        
        if self.response_time_ms is not None and self.response_time_ms < 0:
            raise InvalidPingResultError(
                "Response time cannot be negative"
            )
        
        if self.ttl is not None and self.ttl < 0:
            raise InvalidPingResultError(
                "TTL cannot be negative"
            )
        
        if self.packet_size is not None and self.packet_size < 0:
            raise InvalidPingResultError(
                "Packet size cannot be negative"
            )
    
    @override
    def __str__(self) -> str:
        if self.success:
            return f"Ping successful: {self.response_time_ms:.2f}ms"
        else:
            return f"Ping failed: {self.error_message or 'Unknown error'}"
    

    

