from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadTimeOutError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Timeout(BaseValueObject):
    """
    Value object for ping timeout.
    
    Represents the timeout duration for ping operations in seconds.
    """
    
    value: float
    
    @override
    def _validate(self) -> None:
        """Validate that timeout is positive."""
        if self.value <= 0:
            raise BadTimeOutError("Timeout must be positive")
        
        if self.value > 300:  # 5 minutes max
            raise BadTimeOutError("Timeout cannot exceed 300 seconds")
    
    @override
    def __str__(self) -> str:
        return f"{self.value} s"