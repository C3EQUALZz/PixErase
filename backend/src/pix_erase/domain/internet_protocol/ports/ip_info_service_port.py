from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.ip_info import IPInfo


class IPInfoServicePort(Protocol):
    """
    Protocol for IP information service implementations.
    
    This defines the interface for services that provide
    geographical and network information about IP addresses.
    """
    
    @abstractmethod
    async def get_ip_info(self, ip_address: IPAddress) -> IPInfo:
        """
        Get information about an IP address.
        
        Args:
            ip_address: The IP address to get information for
            
        Returns:
            IPInfo containing geographical and network information
            
        Raises:
            IPInfoConnectionError: If connection to service fails
            IPInfoServiceError: If service returns an error
            IPInfoNotFoundError: If IP information is not found
        """
        raise NotImplementedError

