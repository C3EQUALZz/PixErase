import logging
from dataclasses import dataclass
from typing import final, Final

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.ip_info import IPInfoView
from pix_erase.domain.internet_protocol.errors import PingDestinationUnreachableError
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPAddress, IPInfo, Timeout, PacketSize, TimeToLive, PingResult
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadIPInfoQuery:
    """Command to get information about an IP address."""
    ip_address: str


@final
class ReadIPInfoQueryHandler:
    """
    Handler for getting IP information.
    
    - Opens to everyone.
    - Async processing, non-blocking.
    - Returns IP information including location and network details.
    """
    
    def __init__(
            self,
            internet_service: InternetProtocolService,
            current_user_service: CurrentUserService,
    ) -> None:
        self._internet_service: Final[InternetProtocolService] = internet_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ReadIPInfoQuery) -> IPInfoView:
        """
        Execute get IP info command using domain service.
        
        Args:
            data: Get IP info command data
            
        Returns:
            IPInfoView containing the IP information
        """
        logger.info("Started getting IP info for: %s", data.ip_address)

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        ip_address: IPAddress = self._internet_service.create(data.ip_address)
        logger.info("Created IP address instance: %s", ip_address)

        ping_result: PingResult = await self._internet_service.ping(
            destination=ip_address,
            timeout=Timeout(4),
            packet_size=PacketSize(56),
            ttl=TimeToLive(20)
        )

        if not ping_result.success:
            msg = f"Service with ip: {ip_address.value} unavailable"
            raise PingDestinationUnreachableError(msg)

        # Get IP information
        logger.info("Started fetching IP information")
        ip_info: IPInfo = await self._internet_service.get_ip_info(ip_address)
        logger.info("Got IP info: %s", ip_info)

        # Create view
        view: IPInfoView = IPInfoView(
            ip_address=ip_info.ip_address,
            isp=ip_info.isp,
            organization=ip_info.organization,
            country=ip_info.country,
            region_name=ip_info.region_name,
            city=ip_info.city,
            zip_code=ip_info.zip_code,
            latitude=ip_info.latitude,
            longitude=ip_info.longitude,
            has_location=ip_info.has_location,
            has_network_info=ip_info.has_network_info,
            location_string=ip_info.location_string,
            network_string=ip_info.network_string,
        )

        logger.info("Finished processing IP info view: %s", view)
        return view
