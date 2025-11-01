import asyncio
import logging
from asyncio import Task
from typing import Final, Any

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.internet_protocol.entities.internet_domain import InternetDomain
from pix_erase.domain.internet_protocol.ports.certificate_transparency_port import CertificateTransparencyPort
from pix_erase.domain.internet_protocol.ports.dns_resolver_port import DnsResolverPort
from pix_erase.domain.internet_protocol.ports.domain_id_generator import DomainIdGenerator
from pix_erase.domain.internet_protocol.ports.http_title_fetcher_port import HttpTitleFetcherPort
from pix_erase.domain.internet_protocol.values import DnsRecords, DomainName, Timeout
from pix_erase.domain.internet_protocol.values.domain_id import DomainID

logger: Final[logging.Logger] = logging.getLogger(__name__)


class InternetDomainService(DomainService):
    def __init__(
            self,
            domain_id_generator: DomainIdGenerator,
            dns_resolver: DnsResolverPort,
            certificate_transparency: CertificateTransparencyPort,
            http_title_fetcher: HttpTitleFetcherPort,
    ) -> None:
        super().__init__()
        self._dns_resolver: Final[DnsResolverPort] = dns_resolver
        self._certificate_transparency: Final[CertificateTransparencyPort] = certificate_transparency
        self._http_title_fetcher: Final[HttpTitleFetcherPort] = http_title_fetcher
        self._domain_id_generator: Final[DomainIdGenerator] = domain_id_generator

    async def analyze_domain(self, domain: DomainName, timeout: Timeout) -> InternetDomain:
        background_tasks: set[Task[Any]] = set()
        domain_id: DomainID = self._domain_id_generator()

        logger.debug(
            "Started analyzing domain '%s' with timeout '%s'",
            domain,
            timeout,
        )

        logger.debug("Created dns task for processing domain '%s'", domain)

        dns_task: Task[DnsRecords | None] = asyncio.create_task(
            self._dns_resolver.resolve_records(domain.value)
        )

        background_tasks.add(dns_task)

        logger.debug("Got dns task: %s", dns_task)

        logger.debug("Started creating certificate transparency task for domain '%s'", domain)

        ct_task: Task[list[str]] = asyncio.create_task(
            self._certificate_transparency.fetch_subdomains(
                domain.value,
                timeout=timeout.value
            )
        )
        background_tasks.add(ct_task)

        logger.debug("Got certificate transparency task: %s for domain '%s'", ct_task, domain)

        logger.debug("Started creating http title fetcher task for domain '%s'", domain)

        title_task: Task[str] = asyncio.create_task(
            self._http_title_fetcher.fetch_title(
                domain.value
            )
        )

        logger.debug("Got http title task: %s", title_task)

        dns, subs, title = await asyncio.gather(dns_task, ct_task, title_task)

        dns_task.add_done_callback(background_tasks.discard)
        ct_task.add_done_callback(background_tasks.discard)
        title_task.add_done_callback(background_tasks.discard)

        return InternetDomain(
            id=domain_id,
            domain_name=domain,
            dns_records=dns,
            subdomains=[DomainName(sub) for sub in subs],
            title=title
        )
