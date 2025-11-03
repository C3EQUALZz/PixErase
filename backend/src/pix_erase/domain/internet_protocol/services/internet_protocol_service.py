from ipaddress import ip_address as std_ip_address
from typing import Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidIPAddressError
from pix_erase.domain.internet_protocol.ports.ip_info_service_port import IPInfoServicePort
from pix_erase.domain.internet_protocol.ports.ping_service_port import PingServicePort
from pix_erase.domain.internet_protocol.ports.port_scan_service_port import PortScanServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress, IPv4Address, IPv6Address
from pix_erase.domain.internet_protocol.values.ip_info import IPInfo
from pix_erase.domain.internet_protocol.values.packet_size import PacketSize
from pix_erase.domain.internet_protocol.values.ping_result import PingResult
from pix_erase.domain.internet_protocol.values.port import Port, PortRange
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import PortScanResult, PortScanSummary
from pix_erase.domain.internet_protocol.values.time_to_live import TimeToLive
from pix_erase.domain.internet_protocol.values.timeout import Timeout


class InternetProtocolService(DomainService):
    """
    Domain service for internet protocol operations.
    
    This service encapsulates the business logic for internet protocol operations,
    including IP address creation, validation, and ping operations.
    """

    def __init__(
            self,
            ping_service: PingServicePort,
            ip_info_service: IPInfoServicePort,
            port_scan_service: PortScanServicePort,
    ) -> None:
        super().__init__()
        self._ping_service: Final[PingServicePort] = ping_service
        self._ip_info_service: Final[IPInfoServicePort] = ip_info_service
        self._port_scan_service: Final[PortScanServicePort] = port_scan_service

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
            std_ip = std_ip_address(address)

            if std_ip.version == 4:
                return IPv4Address(value=address)
            if std_ip.version == 6:
                return IPv6Address(value=address)

            msg = f"Unsupported IP version: {std_ip.version}" # type: ignore[unreachable, unused-ignore]
            raise InvalidIPAddressError(msg)

        except ValueError as e:
            msg = f"Invalid IP address format: {address}"
            raise InvalidIPAddressError(msg) from e

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

    async def get_ip_info(self, ip_address: IPAddress) -> IPInfo:
        """
        Get information about an IP address.
        
        Args:
            ip_address: The IP address to get information for
            
        Returns:
            IPInfo containing geographical and network information
        """
        return await self._ip_info_service.get_ip_info(ip_address)

    async def scan_port(
            self,
            target: IPAddress,
            port: Port,
            timeout: Timeout,
    ) -> PortScanResult:
        """
        Scan a single port on a target.
        
        Args:
            target: The target IP address to scan
            port: The port number to scan
            timeout: Timeout in seconds for the connection attempt
            
        Returns:
            PortScanResult containing the scan result
        """
        return await self._port_scan_service.scan_port(
            target=target,
            port=port,
            timeout=timeout.value,
        )

    async def scan_ports(
            self,
            target: IPAddress,
            ports: list[Port],
            timeout: Timeout,
            max_concurrent: int = 100,
    ) -> list[PortScanResult]:
        """
        Scan multiple ports on a target.
        
        Args:
            target: The target IP address to scan
            ports: List of ports to scan
            timeout: Timeout in seconds for each connection attempt
            max_concurrent: Maximum number of concurrent scans
            
        Returns:
            List of PortScanResult objects in the same order as ports
        """
        return await self._port_scan_service.scan_ports(
            target=target,
            ports=ports,
            timeout=timeout.value,
            max_concurrent=max_concurrent,
        )

    async def scan_port_range(
            self,
            target: IPAddress,
            port_range: PortRange,
            timeout: Timeout,
            max_concurrent: int = 100,
    ) -> PortScanSummary:
        """
        Scan a range of ports on a target.
        
        Args:
            target: The target IP address to scan
            port_range: Range of ports to scan
            timeout: Timeout in seconds for each connection attempt
            max_concurrent: Maximum number of concurrent scans
            
        Returns:
            PortScanSummary containing the complete scan results
        """
        return await self._port_scan_service.scan_port_range(
            target=target,
            port_range=port_range,
            timeout=timeout.value,
            max_concurrent=max_concurrent,
        )

    async def scan_common_ports(
            self,
            target: IPAddress,
            timeout: Timeout,
            max_concurrent: int = 100,
    ) -> PortScanSummary:
        """
        Scan common well-known ports (1-1023) on a target.
        
        Args:
            target: The target IP address to scan
            timeout: Timeout in seconds for each connection attempt
            max_concurrent: Maximum number of concurrent scans
            
        Returns:
            PortScanSummary containing the scan results
        """
        return await self._port_scan_service.scan_common_ports(
            target=target,
            timeout=timeout.value,
            max_concurrent=max_concurrent,
        )
