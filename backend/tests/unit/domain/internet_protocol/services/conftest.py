from typing import cast
from unittest.mock import create_autospec

import pytest

from pix_erase.domain.internet_protocol.ports.certificate_transparency_port import CertificateTransparencyPort
from pix_erase.domain.internet_protocol.ports.dns_resolver_port import DnsResolverPort
from pix_erase.domain.internet_protocol.ports.domain_id_generator import DomainIdGenerator
from pix_erase.domain.internet_protocol.ports.http_title_fetcher_port import HttpTitleFetcherPort
from pix_erase.domain.internet_protocol.ports.ip_info_service_port import IPInfoServicePort
from pix_erase.domain.internet_protocol.ports.ping_service_port import PingServicePort
from pix_erase.domain.internet_protocol.ports.port_scan_service_port import PortScanServicePort


@pytest.fixture
def ping_service() -> PingServicePort:
    return cast("PingServicePort", create_autospec(PingServicePort))


@pytest.fixture
def ip_info_service() -> IPInfoServicePort:
    return cast("IPInfoServicePort", create_autospec(IPInfoServicePort))


@pytest.fixture
def port_scan_service() -> PortScanServicePort:
    return cast("PortScanServicePort", create_autospec(PortScanServicePort))


@pytest.fixture
def domain_id_generator() -> DomainIdGenerator:
    return cast("DomainIdGenerator", create_autospec(DomainIdGenerator))


@pytest.fixture
def dns_resolver() -> DnsResolverPort:
    return cast("DnsResolverPort", create_autospec(DnsResolverPort))


@pytest.fixture
def certificate_transparency() -> CertificateTransparencyPort:
    return cast("CertificateTransparencyPort", create_autospec(CertificateTransparencyPort))


@pytest.fixture
def http_title_fetcher() -> HttpTitleFetcherPort:
    return cast("HttpTitleFetcherPort", create_autospec(HttpTitleFetcherPort))

