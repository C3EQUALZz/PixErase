import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.user.errors.user import WrongUserAccountEmailFormatError
from pix_erase.domain.user.values.user_email import UserEmail


@pytest.mark.parametrize(
    "email",
    [
        pytest.param("alice@example.com", id="simple_email"),
        pytest.param("bob.smith@example.com", id="with_dot"),
        pytest.param("user_name@example.co.uk", id="with_underscore"),
        pytest.param("test123@test-domain.org", id="with_numbers_and_hyphen"),
        pytest.param("user+tag@example.com", id="with_plus"),
        pytest.param("user%tag@example.com", id="with_percent"),
        pytest.param("user-name@example.com", id="with_hyphen"),
        pytest.param("a@b.co", id="minimal_valid"),
        pytest.param("very.long.email.address.with.many.parts@very-long-domain-name.example.com", id="long_email"),
        pytest.param("UPPERCASE@EXAMPLE.COM", id="uppercase"),
        pytest.param("MixedCase@Example.Com", id="mixed_case"),
    ],
)
def test_accepts_valid_email(email: str) -> None:
    # Arrange & Act
    sut = UserEmail(email)

    # Assert
    assert sut.value == email
    assert str(sut) == email


@pytest.mark.parametrize(
    ("email", "expected_error"),
    [
        pytest.param("", WrongUserAccountEmailFormatError, id="empty"),
        pytest.param("invalid", WrongUserAccountEmailFormatError, id="no_at_symbol"),
        pytest.param("@example.com", WrongUserAccountEmailFormatError, id="missing_local_part"),
        pytest.param("user@", WrongUserAccountEmailFormatError, id="missing_domain"),
        pytest.param("user@example", WrongUserAccountEmailFormatError, id="missing_tld"),
        pytest.param("user@.com", WrongUserAccountEmailFormatError, id="domain_starts_with_dot"),
        pytest.param("user@example.", WrongUserAccountEmailFormatError, id="domain_ends_with_dot"),
        pytest.param("user@@example.com", WrongUserAccountEmailFormatError, id="double_at"),
        pytest.param("user @example.com", WrongUserAccountEmailFormatError, id="space_in_email"),
        pytest.param("user@exam ple.com", WrongUserAccountEmailFormatError, id="space_in_domain"),
        pytest.param(".user@example.com", WrongUserAccountEmailFormatError, id="starts_with_dot"),
        pytest.param("user.@example.com.", WrongUserAccountEmailFormatError, id="ends_with_dot"),
        pytest.param("user..name@example.com", WrongUserAccountEmailFormatError, id="consecutive_dots"),
        pytest.param("user@example..com", WrongUserAccountEmailFormatError, id="consecutive_dots_in_domain"),
        pytest.param("user@exam#ple.com", WrongUserAccountEmailFormatError, id="invalid_char_in_domain"),
        pytest.param("user#name@example.com", WrongUserAccountEmailFormatError, id="invalid_char_in_local"),
        pytest.param("user@", WrongUserAccountEmailFormatError, id="missing_domain_and_tld"),
    ],
)
def test_rejects_invalid_email(email: str, expected_error: type[DomainFieldError]) -> None:
    # Arrange & Act & Assert
    with pytest.raises(expected_error):
        UserEmail(email)


def test_email_is_immutable() -> None:
    # Arrange
    email = "alice@example.com"
    sut = UserEmail(email)

    # Act & Assert
    assert sut.value == email
    # Проверка что это frozen dataclass уже проверяется в базовом тесте


def test_email_equality() -> None:
    # Arrange
    email = "alice@example.com"
    email1 = UserEmail(email)
    email2 = UserEmail(email)

    # Assert
    assert email1 == email2
    assert hash(email1) == hash(email2)


def test_email_inequality() -> None:
    # Arrange
    email1 = UserEmail("alice@example.com")
    email2 = UserEmail("bob@example.com")

    # Assert
    assert email1 != email2


def test_email_str_representation() -> None:
    # Arrange
    email = "alice@example.com"
    sut = UserEmail(email)

    # Act
    result = str(sut)

    # Assert
    assert result == email
