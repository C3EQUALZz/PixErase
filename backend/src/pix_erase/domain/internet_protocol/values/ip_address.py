from abc import ABC, abstractmethod
from dataclasses import dataclass
from ipaddress import ip_address, IPv4Address as StdIPv4Address, IPv6Address as StdIPv6Address
from typing import override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidIPAddressError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class IPAddress(BaseValueObject, ABC):
    """
    Base value object for IP addresses.
    
    This is an abstract base class that provides common functionality
    for both IPv4 and IPv6 addresses.
    """
    
    value: str
    
    @override
    def _validate(self) -> None:
        """Validate that the IP address is properly formatted."""
        try:
            ip_address(self.value)
        except ValueError as e:
            raise InvalidIPAddressError(f"Invalid IP address format: {self.value}") from e
    
    @override
    def __str__(self) -> str:
        return self.value
    
    @property
    @abstractmethod
    def version(self) -> int:
        """Return the IP version (4 or 6)."""
        raise NotImplementedError
    
    @property
    def is_private(self) -> bool:
        """Check if the IP address is private."""
        return ip_address(self.value).is_private
    
    @property
    def is_loopback(self) -> bool:
        """Check if the IP address is loopback."""
        return ip_address(self.value).is_loopback
    
    @property
    def is_multicast(self) -> bool:
        """Check if the IP address is multicast."""
        return ip_address(self.value).is_multicast
    
    @property
    def is_reserved(self) -> bool:
        """Check if the IP address is reserved."""
        return ip_address(self.value).is_reserved


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class IPv4Address(IPAddress):
    """
    Value object for IPv4 addresses.
    """
    
    @override
    def _validate(self) -> None:
        """Validate that the address is a valid IPv4 address."""
        super()._validate()
        try:
            std_ip = ip_address(self.value)
            if not isinstance(std_ip, StdIPv4Address):
                raise InvalidIPAddressError(f"Expected IPv4 address, got: {self.value}")
        except ValueError as e:
            raise InvalidIPAddressError(f"Invalid IPv4 address format: {self.value}") from e
    
    @property
    @override
    def version(self) -> int:
        return 4


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class IPv6Address(IPAddress):
    """
    Value object for IPv6 addresses.
    """
    
    @override
    def _validate(self) -> None:
        """Validate that the address is a valid IPv6 address."""
        super()._validate()
        try:
            std_ip = ip_address(self.value)
            if not isinstance(std_ip, StdIPv6Address):
                raise InvalidIPAddressError(f"Expected IPv6 address, got: {self.value}")
        except ValueError as e:
            raise InvalidIPAddressError(f"Invalid IPv6 address format: {self.value}") from e
    
    @property
    @override
    def version(self) -> int:
        return 6

