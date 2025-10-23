import aiohttp
import logging
from typing import Final, override

from pix_erase.domain.internet_protocol.errors.internet_protocol import (
    IPInfoConnectionError,
    IPInfoServiceError,
    IPInfoNotFoundError,
)
from pix_erase.domain.internet_protocol.ports.ip_info_service_port import IPInfoServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.ip_info import IPInfo

logger: Final[logging.Logger] = logging.getLogger(__name__)


class IPAPIServicePort(IPInfoServicePort):
    """
    IP-API.com service implementation for IP information.
    
    This implementation uses the ip-api.com service to get
    geographical and network information about IP addresses.
    """

    BASE_URL: Final[str] = "http://ip-api.com/json"

    def __init__(self, timeout: float = 10.0) -> None:
        self._timeout = timeout

    @override
    async def get_ip_info(self, ip_address: IPAddress) -> IPInfo:
        """
        Get information about an IP address using ip-api.com.
        
        Args:
            ip_address: The IP address to get information for
            
        Returns:
            IPInfo containing geographical and network information
            
        Raises:
            IPInfoConnectionError: If connection to service fails
            IPInfoServiceError: If service returns an error
            IPInfoNotFoundError: If IP information is not found
        """
        url = f"{self.BASE_URL}/{ip_address.value}"

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self._timeout)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_response(data)
                    elif response.status == 404:
                        raise IPInfoNotFoundError(f"IP information not found for {ip_address.value}")
                    else:
                        raise IPInfoServiceError(f"Service returned status {response.status}")

        except aiohttp.ClientError as e:
            logger.error(f"Connection error when getting IP info for {ip_address.value}: {e}")
            raise IPInfoConnectionError(f"Failed to connect to IP information service: {e}") from e
        except Exception as e:
            if isinstance(e, (IPInfoConnectionError, IPInfoServiceError, IPInfoNotFoundError)):
                raise
            logger.error(f"Unexpected error when getting IP info for {ip_address.value}: {e}")
            raise IPInfoServiceError(f"Unexpected error: {e}") from e

    @staticmethod
    def _parse_response(data: dict) -> IPInfo:
        """
        Parse the response from ip-api.com service.
        
        Args:
            data: JSON response from the service
            
        Returns:
            IPInfo object with parsed data
            
        Raises:
            IPInfoServiceError: If response format is invalid
        """
        try:
            # Check if the service returned an error
            if data.get("status") == "fail":
                error_message = data.get("message", "Unknown error")
                raise IPInfoServiceError(f"Service error: {error_message}")

            # Extract data with safe defaults
            ip_address = data.get("query", "")
            if not ip_address:
                raise IPInfoServiceError("No IP address in response")

            # Parse coordinates safely
            latitude = data.get("lat")
            longitude = data.get("lon")

            if latitude is not None:
                try:
                    latitude = float(latitude)
                except (ValueError, TypeError):
                    latitude = None

            if longitude is not None:
                try:
                    longitude = float(longitude)
                except (ValueError, TypeError):
                    longitude = None

            return IPInfo(
                ip_address=ip_address,
                isp=data.get("isp"),
                organization=data.get("org"),
                country=data.get("country"),
                region_name=data.get("regionName"),
                city=data.get("city"),
                zip_code=data.get("zip"),
                latitude=latitude,
                longitude=longitude,
            )

        except Exception as e:
            if isinstance(e, IPInfoServiceError):
                raise
            raise IPInfoServiceError(f"Failed to parse service response: {e}") from e

