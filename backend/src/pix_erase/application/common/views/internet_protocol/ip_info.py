from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class IPInfoView:
    """
    View for IP information response.
    
    This view represents the IP information data
    that will be returned to the client.
    """
    
    ip_address: str
    isp: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    region_name: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    has_location: bool = False
    has_network_info: bool = False
    location_string: str = ""
    network_string: str = ""

