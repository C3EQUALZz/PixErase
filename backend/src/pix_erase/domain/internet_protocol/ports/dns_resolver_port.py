from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.internet_protocol.values import DnsRecords


class DnsResolverPort(Protocol):
    @abstractmethod
    async def resolve_records(self, domain: str, lifetime: float = 5.0) -> DnsRecords | None:
        """Return DNS records for the domain."""
        ...
