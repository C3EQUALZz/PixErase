from collections.abc import Generator
from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import BadPortError, BadPortRangeError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class Port(BaseValueObject):
    """
    Represents a network port number.

    Port numbers range from 1 to 65535, with well-known ports (1-1023),
    registered ports (1024-49151), and dynamic/private ports (49152-65535).
    """

    value: int

    @override
    def _validate(self) -> None:
        if not (1 <= self.value <= 65535):
            msg = f"Port number must be between 1 and 65535, got {self.value}"
            raise BadPortError(msg)

    @property
    def is_well_known(self) -> bool:
        """Check if this is a well-known port (1-1023)."""
        return 1 <= self.value <= 1023

    @property
    def is_registered(self) -> bool:
        """Check if this is a registered port (1024-49151)."""
        return 1024 <= self.value <= 49151

    @property
    def is_dynamic(self) -> bool:
        """Check if this is a dynamic/private port (49152-65535)."""
        return 49152 <= self.value <= 65535

    @property
    def category(self) -> str:
        """Get the port category."""
        if self.is_well_known:
            return "well-known"
        if self.is_registered:
            return "registered"
        return "dynamic"

    @override
    def __str__(self) -> str:
        return str(self.value)

    @override
    def __repr__(self) -> str:
        return f"Port({self.value})"


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class PortRange(BaseValueObject):
    """
    Represents a range of ports for scanning.
    """

    start: Port
    end: Port

    @override
    def _validate(self) -> None:
        if self.start.value > self.end.value:
            msg = f"Start port {self.start.value} cannot be greater than end port {self.end.value}"
            raise BadPortRangeError(msg)

    @property
    def count(self) -> int:
        """Get the number of ports in this range."""
        return self.end.value - self.start.value + 1

    def __iter__(self) -> Generator[Port, None, None]:
        """Iterate over all ports in the range."""
        for port_num in range(self.start.value, self.end.value + 1):
            yield Port(port_num)

    @override
    def __str__(self) -> str:
        return f"{self.start.value}-{self.end.value}"

    @override
    def __repr__(self) -> str:
        return f"PortRange({self.start.value}-{self.end.value})"


# Common port ranges
COMMON_PORTS: Final[PortRange] = PortRange(Port(1), Port(1023))
REGISTERED_PORTS: Final[PortRange] = PortRange(Port(1024), Port(49151))
DYNAMIC_PORTS: Final[PortRange] = PortRange(Port(49152), Port(65535))
ALL_PORTS: Final[PortRange] = PortRange(Port(1), Port(65535))

