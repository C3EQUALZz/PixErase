import logging
from typing import Final, override

from pix_erase.domain.internet_protocol.errors.internet_protocol import (
    IPInfoConnectionError,
    IPInfoNotFoundError,
    IPInfoServiceError,
)
from pix_erase.domain.internet_protocol.ports.ip_info_service_port import IPInfoServicePort
from pix_erase.domain.internet_protocol.values.ip_address import IPAddress
from pix_erase.domain.internet_protocol.values.ip_info import IPInfo
from pix_erase.infrastructure.errors.http import HttpError
from pix_erase.infrastructure.http.base import HttpClient

logger: Final[logging.Logger] = logging.getLogger(__name__)


class IPAPIServicePort(IPInfoServicePort):
    """
    IP-API.com service implementation for IP information.

    This implementation uses the ip-api.com service to get
    geographical and network information about IP addresses.
    """

    BASE_URL: Final[str] = "http://ip-api.com/json"

    def __init__(self, http_client: HttpClient) -> None:
        self._http: Final[HttpClient] = http_client
        self._timeout = 20

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
            response = await self._http.get(url, timeout=float(self._timeout))

            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data)
            if response.status_code == 404:
                msg = f"IP information not found for {ip_address.value}"
                raise IPInfoNotFoundError(msg)
            msg = f"Service returned status {response.status_code}"
            raise IPInfoServiceError(msg)

        except HttpError as e:
            logger.exception("Connection error when getting IP info for %s", ip_address.value)
            msg = f"Failed to connect to IP information service: {e}"
            raise IPInfoConnectionError(msg) from e
        except Exception as e:
            if isinstance(e, (IPInfoConnectionError, IPInfoServiceError, IPInfoNotFoundError)):
                raise
            logger.exception("Unexpected error when getting IP info for %s", ip_address.value)
            msg = f"Unexpected error: {e}"
            raise IPInfoServiceError(msg) from e

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
                msg = f"Service error: {error_message}"
                raise IPInfoServiceError(msg)

            # Extract data with safe defaults
            ip_address = data.get("query", "")
            if not ip_address:
                msg = "No IP address in response"
                raise IPInfoServiceError(msg)

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
            msg = f"Failed to parse service response: {e}"
            raise IPInfoServiceError(msg) from e
