import logging
from dataclasses import dataclass
from typing import final, Final

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanView
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPAddress, Port, Timeout
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ScanPortsQuery:
    """Command to scan multiple ports on a target."""
    target: str
    ports: list[int]
    timeout: float = 1.0
    max_concurrent: int = 100


@final
class ScanPortsQueryHandler:
    """
    Handler for scanning multiple ports.
    
    - Opens to everyone.
    - Async processing, non-blocking.
    - Scans multiple ports on target.
    """
    
    def __init__(
        self,
        internet_protocol_service: InternetProtocolService,
        current_user_service: CurrentUserService,
    ) -> None:
        self._internet_protocol_service: Final[InternetProtocolService] = internet_protocol_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ScanPortsQuery) -> list[PortScanView]:
        """
        Execute multiple port scan command using domain service.
        
        Args:
            data: Multiple port scan command data
            
        Returns:
            List of PortScanView containing the scan results
        """
        logger.info(
            "Started multiple port scan for target: %s, ports: %s, timeout: %s, max_concurrent: %s",
            data.target,
            data.ports,
            data.timeout,
            data.max_concurrent,
        )

        logger.info("Getting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user: %s", current_user.id)

        # Create IP address
        ip_address: IPAddress = self._internet_protocol_service.create(data.target)
        logger.info("Created IP address: %s", ip_address)

        # Create ports
        ports = [Port(port_num) for port_num in data.ports]
        logger.info("Created ports: %s", [p.value for p in ports])

        # Create timeout
        timeout: Timeout = Timeout(data.timeout)
        logger.info("Created timeout: %s", timeout)

        # Perform port scan
        logger.info("Starting multiple port scan")
        results = await self._internet_protocol_service.scan_ports(
            target=ip_address,
            ports=ports,
            timeout=timeout,
            max_concurrent=data.max_concurrent,
        )
        logger.info("Multiple port scan completed: %s results", len(results))

        # Create views
        views: list[PortScanView] = [
            PortScanView(
                port=result.port.value,
                status=result.status.value,
                response_time=result.response_time,
                service=result.service,
                error_message=result.error_message,
                scanned_at=result.scanned_at,
            )
            for result in results
        ]

        logger.info("Created %s views", len(views))
        return views

