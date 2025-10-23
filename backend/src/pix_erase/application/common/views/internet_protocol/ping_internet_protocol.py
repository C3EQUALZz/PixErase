from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class PingInternetProtocolView:
    """
    View for ping internet protocol response.
    
    This view represents the response data for ping operations
    that will be returned to the client.
    """
    
    success: bool
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    ttl: Optional[int] = None
    packet_size: Optional[int] = None