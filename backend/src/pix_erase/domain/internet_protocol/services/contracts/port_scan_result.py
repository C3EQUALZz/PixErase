from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pix_erase.domain.internet_protocol.values.port import Port


class PortStatus(Enum):
    """Status of a port during scanning."""
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"
    UNFILTERED = "unfiltered"
    OPEN_FILTERED = "open_filtered"
    CLOSED_FILTERED = "closed_filtered"


@dataclass(frozen=True, slots=True)
class PortScanResult:
    """
    Result of scanning a single port.
    """
    
    port: Port
    status: PortStatus
    response_time: float | None = None
    service: str | None = None
    version: str | None = None
    error_message: str | None = None
    scanned_at: datetime | None = None
    
    @property
    def is_open(self) -> bool:
        """Check if the port is open."""
        return self.status in (PortStatus.OPEN, PortStatus.OPEN_FILTERED)
    
    @property
    def is_closed(self) -> bool:
        """Check if the port is closed."""
        return self.status in (PortStatus.CLOSED, PortStatus.CLOSED_FILTERED)
    
    @property
    def is_filtered(self) -> bool:
        """Check if the port is filtered."""
        return self.status in (PortStatus.FILTERED, PortStatus.OPEN_FILTERED, PortStatus.CLOSED_FILTERED)
    
    def __str__(self) -> str:
        status_str = f"{self.port.value}/{self.status.value}"
        if self.service:
            status_str += f" ({self.service})"
        if self.response_time is not None:
            status_str += f" {self.response_time:.3f}s"
        return status_str
    
    def __repr__(self) -> str:
        return f"PortScanResult(port={self.port.value}, status={self.status.value})"


@dataclass(frozen=True, slots=True)
class PortScanSummary:
    """
    Summary of a port scan operation.
    """
    
    target: str
    port_range: str
    total_ports: int
    open_ports: int
    closed_ports: int
    filtered_ports: int
    scan_duration: float
    started_at: datetime
    completed_at: datetime
    results: list[PortScanResult]
    
    @property
    def open_ports_list(self) -> list[PortScanResult]:
        """Get list of open ports."""
        return [result for result in self.results if result.is_open]
    
    @property
    def closed_ports_list(self) -> list[PortScanResult]:
        """Get list of closed ports."""
        return [result for result in self.results if result.is_closed]
    
    @property
    def filtered_ports_list(self) -> list[PortScanResult]:
        """Get list of filtered ports."""
        return [result for result in self.results if result.is_filtered]
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate of the scan."""
        if self.total_ports == 0:
            return 0.0
        return (self.open_ports + self.closed_ports) / self.total_ports
    
    def __str__(self) -> str:
        return (
            f"Port scan of {self.target} ({self.port_range}): "
            f"{self.open_ports} open, {self.closed_ports} closed, "
            f"{self.filtered_ports} filtered in {self.scan_duration:.2f}s"
        )
    
    def __repr__(self) -> str:
        return f"PortScanSummary(target={self.target}, ports={self.total_ports}, open={self.open_ports})"
