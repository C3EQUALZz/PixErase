import asyncio
import socket
from datetime import datetime
from typing import Final, Coroutine, Mapping

from pix_erase.domain.internet_protocol.errors.internet_protocol import (
    PortScanTimeoutError,
    PortScanPermissionError,
    PortScanNetworkError,
    PortScanConnectionError,
    InvalidPortRangeError,
)
from pix_erase.domain.internet_protocol.ports import PortScanServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.port import Port, PortRange, COMMON_PORTS
from pix_erase.domain.internet_protocol.services.contracts.port_scan_result import (
    PortScanResult,
    PortScanSummary,
    PortStatus,
)


class SocketPortScanServicePort(PortScanServicePort):
    """
    Socket-based implementation of port scanning service.
    
    This implementation uses raw sockets to perform port scanning,
    similar to the provided example code but integrated with the domain architecture.
    """

    def __init__(self) -> None:
        self._max_concurrent: Final[int] = 100

    async def scan_port(
            self,
            target: IPAddress,
            port: Port,
            timeout: float = 1.0,
    ) -> PortScanResult:
        """
        Scan a single port on a target using socket connection.
        
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
        try:
            start_time = datetime.now()

            # Create socket and set timeout
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            try:
                # Attempt to connect
                result = sock.connect_ex((target.value, port.value))
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()

                if result == 0:
                    # Connection successful - port is open
                    status = PortStatus.OPEN
                    service = self._detect_service(port)
                else:
                    # Connection failed - port is closed
                    status = PortStatus.CLOSED
                    service = None

                return PortScanResult(
                    port=port,
                    status=status,
                    response_time=response_time,
                    service=service,
                    scanned_at=start_time,
                )

            finally:
                sock.close()

        except socket.timeout:
            raise PortScanTimeoutError(f"Port scan timed out for {target.value}:{port.value}")
        except PermissionError as e:
            raise PortScanPermissionError(f"Permission denied for port scan: {e}")
        except socket.gaierror as e:
            raise PortScanConnectionError(f"Hostname resolution failed: {e}")
        except OSError as e:
            if e.errno == 13:  # Permission denied
                raise PortScanPermissionError(f"Permission denied for port scan: {e}")
            else:
                raise PortScanNetworkError(f"Network error during port scan: {e}")
        except Exception as e:
            raise PortScanNetworkError(f"Unexpected error during port scan: {e}")

    async def scan_ports(
            self,
            target: IPAddress,
            ports: list[Port],
            timeout: float = 1.0,
            max_concurrent: int = 100,
    ) -> list[PortScanResult]:
        """
        Scan multiple ports on a target concurrently.
        
        Args:
            target: The target IP address to scan
            ports: List of ports to scan
            timeout: Timeout in seconds for each connection attempt
            max_concurrent: Maximum number of concurrent scans
            
        Returns:
            List of PortScanResult objects in the same order as ports
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def scan_single_port(port: Port) -> PortScanResult:
            async with semaphore:
                return await self.scan_port(target, port, timeout)

        tasks: list[Coroutine[None, None, PortScanResult]] = [scan_single_port(port) for port in ports]
        return await asyncio.gather(*tasks)

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
        """
        if port_range.start.value > port_range.end.value:
            raise InvalidPortRangeError(f"Invalid port range: {port_range}")

        start_time = datetime.now()

        # Convert port range to list of ports
        ports = list(port_range)

        # Scan all ports concurrently
        results = await self.scan_ports(
            target=target,
            ports=ports,
            timeout=timeout,
            max_concurrent=max_concurrent,
        )

        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()

        # Count results by status
        open_ports = sum(1 for result in results if isinstance(result, PortScanResult) and result.is_open)
        closed_ports = sum(1 for result in results if isinstance(result, PortScanResult) and result.is_closed)
        filtered_ports = sum(1 for result in results if isinstance(result, PortScanResult) and result.is_filtered)

        return PortScanSummary(
            target=target.value,
            port_range=str(port_range),
            total_ports=len(ports),
            open_ports=open_ports,
            closed_ports=closed_ports,
            filtered_ports=filtered_ports,
            scan_duration=scan_duration,
            started_at=start_time,
            completed_at=end_time,
            results=results,
        )

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
        """
        return await self.scan_port_range(
            target=target,
            port_range=COMMON_PORTS,
            timeout=timeout,
            max_concurrent=max_concurrent,
        )

    @staticmethod
    def _detect_service(port: Port) -> str | None:
        """
        Detect the service running on a port based on common port numbers.
        
        Args:
            port: The port number
            
        Returns:
            Service name if known, None otherwise
        """
        # Common port mappings
        port_services: Final[Mapping[int, str]] = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            3389: "RDP",
            5432: "PostgreSQL",
            3306: "MySQL",
            6379: "Redis",
            27017: "MongoDB",
        }

        return port_services.get(port.value)
