from dataclasses import dataclass
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadTimeToLiveError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class TimeToLive(BaseValueObject):
    """
    Value object for packet time to live (TTL).

    Represents the maximum number of hops a packet can make.
    """

    value: int

    @override
    def _validate(self) -> None:
        """Validate that TTL is within valid range."""
        if self.value < 1:
            msg = "TTL must be at least 1"
            raise BadTimeToLiveError(msg)

        if self.value > 255:
            msg = "TTL cannot exceed 255"
            raise BadTimeToLiveError(msg)

    @override
    def __str__(self) -> str:
        return f"{self.value} s"
