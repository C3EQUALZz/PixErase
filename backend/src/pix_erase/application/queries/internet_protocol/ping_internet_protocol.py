import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.ping_internet_protocol import PingInternetProtocolView
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values.packet_size import PacketSize
from pix_erase.domain.internet_protocol.values.time_to_live import TimeToLive
from pix_erase.domain.internet_protocol.values.timeout import Timeout

if TYPE_CHECKING:
    from pix_erase.domain.internet_protocol.values import IPAddress, PingResult
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class PingInternetProtocolQuery:
    destination_address: str
    timeout: float = 4.0
    packet_size: int = 56
    ttl: int | None = None


@final
class PingInternetProtocolQueryHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Pings IP with ICMP packets.
    """

    def __init__(
        self,
        ping_service: InternetProtocolService,
        current_user_service: CurrentUserService,
    ) -> None:
        self._internet_service: Final[InternetProtocolService] = ping_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: PingInternetProtocolQuery) -> PingInternetProtocolView:
        """
        Execute ping command using domain service.

        Args:
            data: Ping command data

        Returns:
            PingResult containing the ping result information
        """
        logger.info(
            "Started ping for IP: %s with packet size: %s and timeout: %s and ttl: %s",
            data.destination_address,
            data.packet_size,
            data.timeout,
            data.ttl,
        )

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        ip_address: IPAddress = self._internet_service.create(data.destination_address)

        logger.info(
            "Created instance of ip address: %s",
            ip_address,
        )

        logger.info("Started validating timeout: %s", data.timeout)
        timeout: Timeout = Timeout(data.timeout)
        logger.info("Validated timeout: %s", timeout)

        logger.info("Started validating packet size: %s", data.packet_size)
        packet_size: PacketSize = PacketSize(data.packet_size)
        logger.info("Validated packet size: %s", packet_size)

        logger.info("Started validating TTL: %s", data.ttl)
        time_to_live: TimeToLive | None = TimeToLive(data.ttl) if data.ttl else None
        logger.info("Validated TTL: %s", time_to_live)

        logger.info("Started pinging for request")
        ping_result: PingResult = await self._internet_service.ping(
            destination=ip_address,
            timeout=timeout,
            packet_size=packet_size,
            ttl=time_to_live,
        )

        logger.info("Got ping result: %s", ping_result)

        view: PingInternetProtocolView = PingInternetProtocolView(
            success=ping_result.success,
            response_time_ms=ping_result.response_time_ms,
            error_message=ping_result.error_message,
            ttl=ping_result.ttl,
            packet_size=ping_result.packet_size,
        )

        logger.info("Finished processing view: %s", view)

        return view
