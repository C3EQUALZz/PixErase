# ruff: noqa: PLR2004

import pytest

from pix_erase.domain.internet_protocol.entities.internet_domain import InternetDomain
from pix_erase.domain.internet_protocol.ports.certificate_transparency_port import CertificateTransparencyPort
from pix_erase.domain.internet_protocol.ports.dns_resolver_port import DnsResolverPort
from pix_erase.domain.internet_protocol.ports.domain_id_generator import DomainIdGenerator
from pix_erase.domain.internet_protocol.ports.http_title_fetcher_port import HttpTitleFetcherPort
from pix_erase.domain.internet_protocol.services.internet_domain_service import InternetDomainService
from pix_erase.domain.internet_protocol.values.dns_records import DnsRecords
from tests.unit.factories.value_objects import create_domain_id, create_domain_name, create_timeout


@pytest.mark.asyncio
async def test_analyze_domain_creates_domain_with_all_data(
    domain_id_generator: DomainIdGenerator,
    dns_resolver: DnsResolverPort,
    certificate_transparency: CertificateTransparencyPort,
    http_title_fetcher: HttpTitleFetcherPort,
) -> None:
    # Arrange
    expected_domain_id = create_domain_id()
    domain_id_generator.return_value = expected_domain_id

    expected_dns = DnsRecords(
        a=["192.168.1.1"],
        aaaa=[],
        mx=["mail.example.com"],
        ns=["ns1.example.com"],
        txt=["v=spf1"],
        cname=[],
        soa=[],
    )
    dns_resolver.resolve_records.return_value = expected_dns

    expected_subdomains = ["sub1.example.com", "sub2.example.com"]
    certificate_transparency.fetch_subdomains.return_value = expected_subdomains

    expected_title = "Example Domain"
    http_title_fetcher.fetch_title.return_value = expected_title

    sut = InternetDomainService(
        domain_id_generator=domain_id_generator,
        dns_resolver=dns_resolver,
        certificate_transparency=certificate_transparency,
        http_title_fetcher=http_title_fetcher,
    )

    domain_name = create_domain_name("example.com")
    timeout = create_timeout()

    # Act
    result = await sut.analyze_domain(domain_name, timeout)

    # Assert
    assert isinstance(result, InternetDomain)
    assert result.id == expected_domain_id
    assert result.domain_name == domain_name
    assert result.dns_records == expected_dns
    assert len(result.subdomains) == 2
    assert result.subdomains[0].value == "sub1.example.com"
    assert result.subdomains[1].value == "sub2.example.com"
    assert result.title == expected_title
    assert result.is_analyzed is False

    dns_resolver.resolve_records.assert_called_once_with("example.com")
    certificate_transparency.fetch_subdomains.assert_called_once_with(
        "example.com",
        timeout=4.0,
    )
    http_title_fetcher.fetch_title.assert_called_once_with("example.com")


@pytest.mark.asyncio
async def test_analyze_domain_handles_empty_dns_records(
    domain_id_generator: DomainIdGenerator,
    dns_resolver: DnsResolverPort,
    certificate_transparency: CertificateTransparencyPort,
    http_title_fetcher: HttpTitleFetcherPort,
) -> None:
    # Arrange
    expected_domain_id = create_domain_id()
    domain_id_generator.return_value = expected_domain_id

    dns_resolver.resolve_records.return_value = None

    certificate_transparency.fetch_subdomains.return_value = []

    http_title_fetcher.fetch_title.return_value = None

    sut = InternetDomainService(
        domain_id_generator=domain_id_generator,
        dns_resolver=dns_resolver,
        certificate_transparency=certificate_transparency,
        http_title_fetcher=http_title_fetcher,
    )

    domain_name = create_domain_name("example.com")
    timeout = create_timeout()

    # Act
    result = await sut.analyze_domain(domain_name, timeout)

    # Assert
    assert result.dns_records is None
    assert result.subdomains == []
    assert result.title is None


@pytest.mark.asyncio
async def test_analyze_domain_handles_no_subdomains(
    domain_id_generator: DomainIdGenerator,
    dns_resolver: DnsResolverPort,
    certificate_transparency: CertificateTransparencyPort,
    http_title_fetcher: HttpTitleFetcherPort,
) -> None:
    # Arrange
    domain_id_generator.return_value = create_domain_id()

    dns_resolver.resolve_records.return_value = None

    certificate_transparency.fetch_subdomains.return_value = []

    http_title_fetcher.fetch_title.return_value = "Example"

    sut = InternetDomainService(
        domain_id_generator=domain_id_generator,
        dns_resolver=dns_resolver,
        certificate_transparency=certificate_transparency,
        http_title_fetcher=http_title_fetcher,
    )

    domain_name = create_domain_name("example.com")
    timeout = create_timeout()

    # Act
    result = await sut.analyze_domain(domain_name, timeout)

    # Assert
    assert result.subdomains == []
    assert result.title == "Example"
