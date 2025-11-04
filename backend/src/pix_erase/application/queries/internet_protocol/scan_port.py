import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanView
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPAddress, Port, Timeout

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ScanPortQuery:
    """Command to scan a single port on a target."""

    target: str
    port: int
    timeout: float = 1.0


@final
class ScanPortQueryHandler:
    """
    Scan a single port on a target IP address or hostname
    It's useful for checking if a specific service is running on a target.

    - Opens to everyone.
    - Async processing, non-blocking.
    - Scans a single port on target.
    """

    def __init__(
        self,
        internet_protocol_service: InternetProtocolService,
        current_user_service: CurrentUserService,
    ) -> None:
        self._internet_protocol_service: Final[InternetProtocolService] = internet_protocol_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ScanPortQuery) -> PortScanView:
        """
        Execute port scan command using domain service.

        Args:
            data: Port scan command data

        Returns:
            PortScanView containing the scan result
        """
        logger.info(
            "Started port scan for target: %s, port: %s, timeout: %s",
            data.target,
            data.port,
            data.timeout,
        )

        logger.info("Getting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user: %s", current_user.id)

        # Create IP address
        ip_address: IPAddress = self._internet_protocol_service.create(data.target)
        logger.info("Created IP address: %s", ip_address)

        # Create port
        port: Port = Port(data.port)
        logger.info("Created port: %s", port)

        # Create timeout
        timeout: Timeout = Timeout(data.timeout)
        logger.info("Created timeout: %s", timeout)

        # Perform port scan
        logger.info("Starting port scan")
        result = await self._internet_protocol_service.scan_port(
            target=ip_address,
            port=port,
            timeout=timeout,
        )
        logger.info("Port scan completed: %s", result)

        # Create view
        view: PortScanView = PortScanView(
            port=result.port.value,
            status=result.status.value,
            response_time=result.response_time,
            service=result.service,
            error_message=result.error_message,
            scanned_at=result.scanned_at,
        )

        logger.info("Created view: %s", view)
        return view
