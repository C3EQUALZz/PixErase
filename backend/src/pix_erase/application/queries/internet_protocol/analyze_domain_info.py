import logging
from dataclasses import dataclass
from typing import Final, final, cast

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.analyze_domain import AnalyzeDomainView
from pix_erase.domain.internet_protocol.entities.internet_domain import InternetDomain
from pix_erase.domain.internet_protocol.services.internet_domain_service import InternetDomainService
from pix_erase.domain.internet_protocol.values import Timeout, DomainName
from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True, frozen=True)
class AnalyzeDomainQuery:
    domain: str
    timeout: float = 10


@final
class AnalyzeDomainQueryHandler:
    """
    - Opens to everyone.
    - Async processing, non-blocking.
    - Analyzing existing domain. 
    """
    def __init__(
            self,
            current_user_service: CurrentUserService,
            internet_domain_service: InternetDomainService
    ) -> None:
        self._internet_domain_service: Final[InternetDomainService] =  internet_domain_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: AnalyzeDomainQuery) -> AnalyzeDomainView:
        logger.info(
            "Started processing domain: %s with timeout: %s",
            data.domain,
            data.timeout,
        )

        logger.info("Started timeout validation: %s", data.timeout)
        timeout: Timeout = Timeout(data.timeout)
        logger.info("Timeout validated: %s", timeout)

        logger.info("Started domain nama validation: %s", data.domain)
        domain: DomainName = DomainName(data.domain)
        logger.info("Domain validated: %s", domain)

        logger.info("Getting current user id")
        current_user: User = await self._current_user_service.get_current_user()
        logger.info("Successfully got current user id: %s", current_user.id)

        info_for_domain: InternetDomain = await self._internet_domain_service.analyze_domain(
            domain=domain,
            timeout=timeout,
        )

        return AnalyzeDomainView(
            domain_id=info_for_domain.id,
            domain_name=str(info_for_domain.domain_name),
            dns_records=cast(dict[str, list[str]], info_for_domain.dns_records.to_dict()) if info_for_domain.dns_records else None,
            subdomains=[str(subdomain) for subdomain in info_for_domain.subdomains],
            title=info_for_domain.title,
            created_at=info_for_domain.created_at,
            updated_at=info_for_domain.updated_at,
        )

