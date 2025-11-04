from dataclasses import dataclass, field

from pix_erase.domain.common.entities.base_aggregate import BaseAggregateRoot
from pix_erase.domain.internet_protocol.values import DnsRecords, DomainName
from pix_erase.domain.internet_protocol.values.domain_id import DomainID


@dataclass(eq=False, kw_only=True)
class InternetDomain(BaseAggregateRoot[DomainID]):
    """
    Aggregate representing a domain for internet protocol operations.

    This entity encapsulates domain-related data and provides domain-specific
    business logic for OSINT operations, DNS queries, and domain analysis.

    Attributes:
        domain_name: The validated domain name value object
        dns_records: Cached DNS records for the domain (optional)
        subdomains: List of discovered subdomains
        title: HTTP title of the domain (optional)
        is_analyzed: Flag indicating if domain has been analyzed
    """

    domain_name: DomainName
    dns_records: DnsRecords | None = field(default=None)
    subdomains: list[DomainName] = field(default_factory=list)
    title: str | None = field(default=None)
    is_analyzed: bool = field(default=False)

    @property
    def tld(self) -> str:
        """Get the top-level domain (TLD)."""
        return self.domain_name.tld

    @property
    def root_domain(self) -> str:
        """Get the root domain (last two labels)."""
        return self.domain_name.root_domain

    @property
    def labels(self) -> list[str]:
        """Get all domain labels (parts separated by dots)."""
        return self.domain_name.labels

    @property
    def has_dns_records(self) -> bool:
        """Check if DNS records are available."""
        return self.dns_records is not None

    @property
    def has_subdomains(self) -> bool:
        """Check if any subdomains were discovered."""
        return len(self.subdomains) > 0

    @property
    def subdomain_count(self) -> int:
        """Get the count of discovered subdomains."""
        return len(self.subdomains)

    # Business logic methods
    def update_dns_records(self, dns_records: DnsRecords) -> None:
        """
        Update DNS records for the domain.

        Args:
            dns_records: Dictionary of DNS record types to values

        Note:
            This method mutates the entity and should be called within
            a domain service that handles business rules and events.
        """
        self.dns_records = dns_records
        if not self.is_analyzed:
            self.is_analyzed = True

    def add_subdomains(self, subdomains: list[DomainName]) -> None:
        """
        Add discovered subdomains to the domain.

        Args:
            subdomains: List of subdomain names to add

        Note:
            - Prevents duplicates
            - Should be called within a domain service
        """
        # Add only new subdomains to avoid duplicates
        existing = set(self.subdomains)
        new_subdomains = [sub for sub in subdomains if sub not in existing]
        self.subdomains.extend(new_subdomains)

        if new_subdomains and not self.is_analyzed:
            self.is_analyzed = True

    def update_title(self, title: str) -> None:
        """
        Update the HTTP title of the domain.

        Args:
            title: The HTTP title text

        Note:
            Should be called within a domain service
        """
        self.title = title
        if not self.is_analyzed:
            self.is_analyzed = True

    def mark_as_analyzed(self) -> None:
        """
        Mark the domain as analyzed.

        Note:
            Should be called when OSINT analysis is complete
        """
        self.is_analyzed = True
