from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.port import Port, PortRange
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import PortScanResult, PortScanSummary


class PortScanServicePort(Protocol):
    """
    Protocol for port scanning service implementations.
    
    This defines the interface that port scanning service implementations must follow.
    It allows for different implementations (socket-based, external tools, etc.)
    while maintaining a consistent interface.
    """
    
    @abstractmethod
    async def scan_port(
        self,
        target: IPAddress,
        port: Port,
        timeout: float = 1.0,
    ) -> PortScanResult:
        """
        Scan a single port on a target.
        
        Args:
            target: The target IP address to scan
            port: The port number to scan
            timeout: Timeout in seconds for the connection attempt
            
        Returns:
            PortScanResult containing the scan result
            
        Raises:
            PortScanTimeoutError: If the scan times out
            PortScanPermissionError: If elevated permissions are required
            PortScanNetworkError: If a network error occurs
            PortScanConnectionError: If connection to target fails
        """
        raise NotImplementedError
    
    @abstractmethod
    async def scan_ports(
        self,
        target: IPAddress,
        ports: list[Port],
        timeout: float = 1.0,
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
            
        Raises:
            PortScanTimeoutError: If the scan times out
            PortScanPermissionError: If elevated permissions are required
            PortScanNetworkError: If a network error occurs
            PortScanConnectionError: If connection to target fails
        """
        raise NotImplementedError
    
    @abstractmethod
    async def scan_port_range(
        self,
        target: IPAddress,
        port_range: PortRange,
        timeout: float = 1.0,
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
            
        Raises:
            PortScanTimeoutError: If the scan times out
            PortScanPermissionError: If elevated permissions are required
            PortScanNetworkError: If a network error occurs
            PortScanConnectionError: If connection to target fails
            InvalidPortRangeError: If port range is invalid
        """
        raise NotImplementedError
    
    @abstractmethod
    async def scan_common_ports(
        self,
        target: IPAddress,
        timeout: float = 1.0,
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
            
        Raises:
            PortScanTimeoutError: If the scan times out
            PortScanPermissionError: If elevated permissions are required
            PortScanNetworkError: If a network error occurs
            PortScanConnectionError: If connection to target fails
        """
        raise NotImplementedError

