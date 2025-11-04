from pix_erase.domain.internet_protocol.entities.internet_domain import InternetDomain
from pix_erase.domain.internet_protocol.values.dns_records import DnsRecords
from pix_erase.domain.internet_protocol.values.domain_id import DomainID
from pix_erase.domain.internet_protocol.values.domain_name import DomainName
from tests.unit.factories.value_objects import create_domain_id, create_domain_name


def create_internet_domain(
    domain_id: DomainID | None = None,
    domain_name: DomainName | None = None,
    dns_records: DnsRecords | None = None,
    subdomains: list[DomainName] | None = None,
    title: str | None = None,
    is_analyzed: bool | None = None,
) -> InternetDomain:
    if is_analyzed is None:
        is_analyzed = False

    return InternetDomain(
        id=domain_id or create_domain_id(),
        domain_name=domain_name or create_domain_name(),
        dns_records=dns_records,
        subdomains=subdomains or [],
        title=title,
        is_analyzed=is_analyzed,
    )
