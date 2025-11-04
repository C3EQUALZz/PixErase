from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.ping_result import PingResult


class PingServicePort(Protocol):
    """
    Protocol for ping service implementations.

    This defines the interface that ping service implementations must follow.
    It allows for different implementations (raw sockets, external libraries, etc.)
    while maintaining a consistent interface.
    """

    @abstractmethod
    async def ping(
        self,
        destination: IPAddress,
        timeout: float = 4.0,
        packet_size: int = 56,
        ttl: int | None = None,
    ) -> PingResult:
        """
        Ping a destination IP address.

        Args:
            destination: The IP address to ping
            timeout: Timeout in seconds
            packet_size: Size of the ping packet in bytes
            ttl: Time to live for the packet

        Returns:
            PingResult containing the ping result information

        Raises:
            PingTimeoutError: If the ping times out
            PingDestinationUnreachableError: If destination is unreachable
            PingTimeExceededError: If TTL is exceeded
            PingPermissionError: If elevated permissions are required
            PingNetworkError: If a network error occurs
        """
        raise NotImplementedError

    @abstractmethod
    async def ping_multiple(
        self,
        destinations: list[IPAddress],
        timeout: float = 4.0,
        packet_size: int = 56,
        ttl: int | None = None,
    ) -> list[PingResult]:
        """
        Ping multiple destination IP addresses.

        Args:
            destinations: List of IP addresses to ping
            timeout: Timeout in seconds for each ping
            packet_size: Size of the ping packet in bytes
            ttl: Time to live for the packet

        Returns:
            List of PingResult objects in the same order as destinations
        """
        raise NotImplementedError
