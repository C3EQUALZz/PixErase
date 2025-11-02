from pix_erase.domain.internet_protocol.values.dns_records import DnsRecords
from pix_erase.domain.internet_protocol.values.domain_name import DomainName
from tests.unit.factories.internet_protocol_entity import create_internet_domain
from tests.unit.factories.value_objects import create_domain_name


def test_creates_domain_with_default_values() -> None:
    # Arrange
    domain_name = create_domain_name("example.com")

    # Act
    sut = create_internet_domain(domain_name=domain_name)

    # Assert
    assert sut.domain_name == domain_name
    assert sut.dns_records is None
    assert sut.subdomains == []
    assert sut.title is None
    assert sut.is_analyzed is False


def test_tld_property() -> None:
    # Arrange
    domain_name = create_domain_name("subdomain.example.com")
    sut = create_internet_domain(domain_name=domain_name)

    # Act
    result = sut.tld

    # Assert
    assert result == "com"


def test_root_domain_property() -> None:
    # Arrange
    domain_name = create_domain_name("subdomain.example.com")
    sut = create_internet_domain(domain_name=domain_name)

    # Act
    result = sut.root_domain

    # Assert
    assert result == "example.com"


def test_labels_property() -> None:
    # Arrange
    domain_name = create_domain_name("subdomain.example.com")
    sut = create_internet_domain(domain_name=domain_name)

    # Act
    result = sut.labels

    # Assert
    assert result == ["subdomain", "example", "com"]


def test_has_dns_records_property_true() -> None:
    # Arrange
    dns_records = DnsRecords(
        a=["192.168.1.1"],
        aaaa=[],
        mx=[],
        ns=[],
        txt=[],
        cname=[],
        soa=[],
    )
    sut = create_internet_domain(dns_records=dns_records)

    # Act
    result = sut.has_dns_records

    # Assert
    assert result is True


def test_has_dns_records_property_false() -> None:
    # Arrange
    sut = create_internet_domain()

    # Act
    result = sut.has_dns_records

    # Assert
    assert result is False


def test_has_subdomains_property_true() -> None:
    # Arrange
    subdomains = [create_domain_name("sub1.example.com"), create_domain_name("sub2.example.com")]
    sut = create_internet_domain(subdomains=subdomains)

    # Act
    result = sut.has_subdomains

    # Assert
    assert result is True


def test_has_subdomains_property_false() -> None:
    # Arrange
    sut = create_internet_domain()

    # Act
    result = sut.has_subdomains

    # Assert
    assert result is False


def test_subdomain_count_property() -> None:
    # Arrange
    subdomains = [create_domain_name("sub1.example.com"), create_domain_name("sub2.example.com")]
    sut = create_internet_domain(subdomains=subdomains)

    # Act
    result = sut.subdomain_count

    # Assert
    assert result == 2


def test_update_dns_records() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=False)
    dns_records = DnsRecords(
        a=["192.168.1.1"],
        aaaa=[],
        mx=[],
        ns=[],
        txt=[],
        cname=[],
        soa=[],
    )

    # Act
    sut.update_dns_records(dns_records)

    # Assert
    assert sut.dns_records == dns_records
    assert sut.is_analyzed is True


def test_update_dns_records_preserves_analyzed_flag() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=True)
    dns_records = DnsRecords(
        a=["192.168.1.1"],
        aaaa=[],
        mx=[],
        ns=[],
        txt=[],
        cname=[],
        soa=[],
    )

    # Act
    sut.update_dns_records(dns_records)

    # Assert
    assert sut.dns_records == dns_records
    assert sut.is_analyzed is True


def test_add_subdomains() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=False)
    new_subdomains = [create_domain_name("sub1.example.com"), create_domain_name("sub2.example.com")]

    # Act
    sut.add_subdomains(new_subdomains)

    # Assert
    assert len(sut.subdomains) == 2
    assert sut.subdomains == new_subdomains
    assert sut.is_analyzed is True


def test_add_subdomains_preserves_analyzed_flag() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=True)
    new_subdomains = [create_domain_name("sub1.example.com")]

    # Act
    sut.add_subdomains(new_subdomains)

    # Assert
    assert len(sut.subdomains) == 1
    assert sut.is_analyzed is True


def test_add_subdomains_prevents_duplicates() -> None:
    # Arrange
    existing_subdomain = create_domain_name("sub1.example.com")
    sut = create_internet_domain(subdomains=[existing_subdomain])
    new_subdomains = [existing_subdomain, create_domain_name("sub2.example.com")]

    # Act
    sut.add_subdomains(new_subdomains)

    # Assert
    assert len(sut.subdomains) == 2
    assert sut.subdomains[0] == existing_subdomain
    assert sut.subdomains[1] == create_domain_name("sub2.example.com")


def test_update_title() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=False)
    title = "Example Domain"

    # Act
    sut.update_title(title)

    # Assert
    assert sut.title == title
    assert sut.is_analyzed is True


def test_update_title_preserves_analyzed_flag() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=True)
    title = "Example Domain"

    # Act
    sut.update_title(title)

    # Assert
    assert sut.title == title
    assert sut.is_analyzed is True


def test_mark_as_analyzed() -> None:
    # Arrange
    sut = create_internet_domain(is_analyzed=False)

    # Act
    sut.mark_as_analyzed()

    # Assert
    assert sut.is_analyzed is True

