import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidDomainNameError
from pix_erase.domain.internet_protocol.values.domain_name import DomainName, MAX_DOMAIN_LENGTH
from tests.unit.factories.value_objects import create_domain_name


@pytest.mark.parametrize(
    "domain",
    [
        pytest.param("example.com", id="simple_domain"),
        pytest.param("subdomain.example.com", id="with_subdomain"),
        pytest.param("a.b.c.example.com", id="multiple_subdomains"),
        pytest.param("example.co.uk", id="multi_tld"),
        pytest.param("test-domain.com", id="with_hyphen"),
        pytest.param("test123.com", id="with_numbers"),
        pytest.param("a.co", id="minimal_domain"),
    ],
)
def test_accepts_valid_domain(domain: str) -> None:
    # Arrange & Act
    sut = DomainName(value=domain)

    # Assert
    assert sut.value == domain
    assert str(sut) == domain


@pytest.mark.parametrize(
    ("domain", "expected_error"),
    [
        pytest.param("", InvalidDomainNameError, id="empty"),
        pytest.param("   ", InvalidDomainNameError, id="whitespace_only"),
        pytest.param("example", InvalidDomainNameError, id="no_tld"),
        pytest.param(".example.com", InvalidDomainNameError, id="starts_with_dot"),
        pytest.param("example.com.", InvalidDomainNameError, id="ends_with_dot"),
        pytest.param("-example.com", InvalidDomainNameError, id="starts_with_hyphen"),
        pytest.param("example-.com", InvalidDomainNameError, id="ends_with_hyphen_in_label"),
        pytest.param("example..com", InvalidDomainNameError, id="consecutive_dots"),
        pytest.param("a" * (MAX_DOMAIN_LENGTH + 1) + ".com", InvalidDomainNameError, id="too_long"),
        pytest.param("example.c", InvalidDomainNameError, id="tld_too_short"),
        pytest.param("a" * 64 + ".com", InvalidDomainNameError, id="label_too_long"),
    ],
)
def test_rejects_invalid_domain(domain: str, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        DomainName(value=domain)


def test_labels_property() -> None:
    # Arrange
    domain = "subdomain.example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.labels

    # Assert
    assert result == ["subdomain", "example", "com"]


def test_tld_property() -> None:
    # Arrange
    domain = "subdomain.example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.tld

    # Assert
    assert result == "com"


def test_root_domain_property() -> None:
    # Arrange
    domain = "subdomain.example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.root_domain

    # Assert
    assert result == "example.com"


def test_root_domain_property_single_label() -> None:
    # Arrange
    domain = "example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.root_domain

    # Assert
    assert result == "example.com"


def test_is_subdomain_property() -> None:
    # Arrange
    domain = "subdomain.example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.is_subdomain

    # Assert
    assert result is True


def test_is_subdomain_property_false() -> None:
    # Arrange
    domain = "example.com"
    sut = create_domain_name(domain)

    # Act
    result = sut.is_subdomain

    # Assert
    assert result is False


def test_domain_name_equality() -> None:
    # Arrange
    domain = "example.com"
    domain1 = DomainName(value=domain)
    domain2 = DomainName(value=domain)

    # Assert
    assert domain1 == domain2
    assert hash(domain1) == hash(domain2)


def test_domain_name_inequality() -> None:
    # Arrange
    domain1 = create_domain_name("example.com")
    domain2 = create_domain_name("example.org")

    # Assert
    assert domain1 != domain2


