from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadPackageSizeError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class PacketSize(BaseValueObject):
    """
    Value object for ping packet size.
    
    Represents the size of ping packets in bytes.
    """
    
    value: int
    
    @override
    def _validate(self) -> None:
        """Validate that packet size is within valid range."""
        if self.value < 8:  # Minimum size for timestamp
            raise BadPackageSizeError("Packet size must be at least 8 bytes")
        
        if self.value > 1500:  # Typical MTU
            raise BadPackageSizeError("Packet size cannot exceed 1500 bytes")
    
    @override
    def __str__(self) -> str:
        return f"{self.value} bytes"