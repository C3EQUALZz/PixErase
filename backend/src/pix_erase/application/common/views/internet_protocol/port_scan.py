from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class PortScanView:
    """
    View for single port scan response.
    
    This view represents the response data for single port scan operations
    that will be returned to the client.
    """
    
    port: int
    status: str
    response_time: Optional[float] = None
    service: Optional[str] = None
    error_message: Optional[str] = None
    scanned_at: Optional[datetime] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class PortScanSummaryView:
    """
    View for port scan summary response.
    
    This view represents the summary data for port scan operations
    that will be returned to the client.
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
    success_rate: float
    results: list[dict[str, Any]]

