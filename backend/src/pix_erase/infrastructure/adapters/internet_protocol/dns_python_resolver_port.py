import logging
from typing import Final, override

import dns.resolver
from dns.resolver import LifetimeTimeout

from pix_erase.domain.internet_protocol.ports.dns_resolver_port import DnsResolverPort
from pix_erase.domain.internet_protocol.values.dns_records import DnsRecords, DnsRecordsDict

logger: Final[logging.Logger] = logging.getLogger(__name__)


class DnsPythonResolverPort(DnsResolverPort):
    def __init__(self) -> None:
        self._resolver: Final[dns.resolver.Resolver] = dns.resolver.Resolver()

    @override
    async def resolve_records(self, domain: str, lifetime: float = 5.0) -> DnsRecords | None:
        logger.debug("Started resolving records for domain: %s with lifetime: %s seconds", domain, lifetime)

        records: DnsRecordsDict = {"A": [], "AAAA": [], "MX": [], "NS": [], "TXT": [], "CNAME": [], "SOA": []}

        for rr in records:
            logger.debug("Processing record: %s", rr)

            try:
                answers = self._resolver.resolve(domain, rr, lifetime=lifetime)
                logger.debug("Got answers: %s", answers)

                records[rr] = [r.to_text() for r in answers]  # type: ignore[literal-required]

            except LifetimeTimeout:
                records[rr] = []  # type: ignore[literal-required]

            except dns.resolver.NXDOMAIN:
                logger.exception("Got NXDOMAIN for domain: %s with lifetime: %s seconds", domain, lifetime)
                return None

        return DnsRecords.from_dict(records)
