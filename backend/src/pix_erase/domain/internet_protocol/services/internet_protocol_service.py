from typing import Final, override

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.internet_protocol.ports.ping_service_port import PingServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress, IPv4Address, IPv6Address
from pix_erase.domain.internet_protocol.values.ping_result import PingResult
from pix_erase.domain.internet_protocol.values.timeout import Timeout
from pix_erase.domain.internet_protocol.values.packet_size import PacketSize
from pix_erase.domain.internet_protocol.values.time_to_live import TimeToLive
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidIPAddressError


class InternetProtocolService(DomainService):
    """
    Domain service for internet protocol operations.
    
    This service encapsulates the business logic for internet protocol operations,
    including IP address creation, validation, and ping operations.
    """
    
    def __init__(
        self,
        ping_service: PingServicePort,
    ) -> None:
        super().__init__()
        self._ping_service: Final[PingServicePort] = ping_service
    
    def create(self, address: str) -> IPAddress:
        """
        Create an IP address from string.
        
        Args:
            address: IP address string
            
        Returns:
            IPv4Address or IPv6Address
            
        Raises:
            InvalidIPAddressError: If address format is invalid
        """
        try:
            from ipaddress import ip_address as std_ip_address
            std_ip = std_ip_address(address)
            
            if std_ip.version == 4:
                return IPv4Address(value=address)
            elif std_ip.version == 6:
                return IPv6Address(value=address)
            else:
                raise InvalidIPAddressError(f"Unsupported IP version: {std_ip.version}")
        except ValueError as e:
            raise InvalidIPAddressError(f"Invalid IP address format: {address}") from e
    
    async def ping(
        self,
        destination: IPAddress,
        timeout: Timeout,
        packet_size: PacketSize,
        ttl: TimeToLive | None = None,
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
        """
        return await self._ping_service.ping(
            destination=destination,
            timeout=timeout.value,
            packet_size=packet_size.value,
            ttl=ttl.value if ttl else None,
        )
    
    async def ping_multiple(
        self,
        destinations: list[IPAddress],
        timeout: Timeout,
        packet_size: PacketSize,
        ttl: TimeToLive | None = None,
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
        return await self._ping_service.ping_multiple(
            destinations=destinations,
            timeout=timeout.value,
            packet_size=packet_size.value,
            ttl=ttl.value if ttl else None,
        )