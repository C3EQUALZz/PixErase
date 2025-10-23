from dataclasses import dataclass
from typing import Optional, override

from pix_erase.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class IPInfo(BaseValueObject):
    """
    Value object containing information about an IP address.
    
    This represents geographical and network information
    retrieved from external IP geolocation services.
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
    
    @override
    def _validate(self) -> None:
        """Validate IP information data."""
        if not self.ip_address:
            raise ValueError("IP address cannot be empty")
        
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
    
    @override
    def __str__(self) -> str:
        location_parts = []
        if self.city:
            location_parts.append(self.city)
        if self.region_name:
            location_parts.append(self.region_name)
        if self.country:
            location_parts.append(self.country)
        
        location = ", ".join(location_parts) if location_parts else "Unknown location"
        return f"{self.ip_address} ({location})"
    
    @property
    def has_location(self) -> bool:
        """Check if location information is available."""
        return self.latitude is not None and self.longitude is not None
    
    @property
    def has_network_info(self) -> bool:
        """Check if network information is available."""
        return self.isp is not None or self.organization is not None
    
    @property
    def location_string(self) -> str:
        """Get formatted location string."""
        parts = []
        if self.city:
            parts.append(self.city)
        if self.region_name:
            parts.append(self.region_name)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts) if parts else "Unknown"
    
    @property
    def network_string(self) -> str:
        """Get formatted network information string."""
        if self.isp and self.organization:
            return f"{self.isp} ({self.organization})"
        elif self.isp:
            return self.isp
        elif self.organization:
            return self.organization
        else:
            return "Unknown"

