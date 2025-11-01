import logging
from dataclasses import dataclass
from typing import final, Final

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.port_scan import PortScanSummaryView
from pix_erase.domain.internet_protocol.services.internet_protocol_service import InternetProtocolService
from pix_erase.domain.internet_protocol.values import IPAddress, Timeout
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ScanCommonPortsQuery:
    """Command to scan common well-known ports on a target."""
    target: str
    timeout: float = 1.0
    max_concurrent: int = 100


@final
class ScanCommonPortsQueryHandler:
    """
    Scan common well-known ports (1-1023) on a target IP address or hostname.
    It's useful for a quick security assessment of a target.
    
    - Opens to everyone.
    - Async processing, non-blocking.
    - Scans common ports (1-1023) on target.
    """
    
    def __init__(
        self,
        internet_protocol_service: InternetProtocolService,
        current_user_service: CurrentUserService,
    ) -> None:
        self._internet_protocol_service: Final[InternetProtocolService] = internet_protocol_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ScanCommonPortsQuery) -> PortScanSummaryView:
        """
        Execute common ports scan command using domain service.
        
        Args:
            data: Common ports scan command data
            
        Returns:
            PortScanSummaryView containing the scan summary
        """
        logger.info(
            "Started common ports scan for target: %s, timeout: %s, max_concurrent: %s",
            data.target,
            data.timeout,
            data.max_concurrent,
        )

        logger.info("Getting current user")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user: %s", current_user.id)

        # Create IP address
        ip_address: IPAddress = self._internet_protocol_service.create(data.target)
        logger.info("Created IP address: %s", ip_address)

        # Create timeout
        timeout: Timeout = Timeout(data.timeout)
        logger.info("Created timeout: %s", timeout)

        # Perform common ports scan
        logger.info("Starting common ports scan")
        summary = await self._internet_protocol_service.scan_common_ports(
            target=ip_address,
            timeout=timeout,
            max_concurrent=data.max_concurrent,
        )
        logger.info("Common ports scan completed: %s", summary)

        # Create view
        view: PortScanSummaryView = PortScanSummaryView(
            target=summary.target,
            port_range=summary.port_range,
            total_ports=summary.total_ports,
            open_ports=summary.open_ports,
            closed_ports=summary.closed_ports,
            filtered_ports=summary.filtered_ports,
            scan_duration=summary.scan_duration,
            started_at=summary.started_at,
            completed_at=summary.completed_at,
            success_rate=summary.success_rate,
            results=[
                {
                    "port": result.port.value,
                    "status": result.status.value,
                    "response_time": result.response_time,
                    "service": result.service,
                    "error_message": result.error_message,
                    "scanned_at": result.scanned_at,
                }
                for result in summary.results
            ],
        )

        logger.info("Created view: %s", view)
        return view

