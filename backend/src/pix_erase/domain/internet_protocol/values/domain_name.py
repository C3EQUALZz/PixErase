import re
from dataclasses import dataclass
from typing import Final, override

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.errors.internet_protocol import InvalidDomainNameError

# RFC 1123 compliant domain name regex
# Allows hostnames with length 1-253 characters
# Each label can be 1-63 characters
# Labels can contain letters, digits, and hyphens
# Hyphens cannot be at the beginning or end of a label
# TLD must be at least 2 characters
DOMAIN_NAME_REGEX: Final[re.Pattern[str]] = re.compile(
    r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$',
    re.IGNORECASE
)

# Maximum domain name length (including dots)
MAX_DOMAIN_LENGTH: Final[int] = 253


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class DomainName(BaseValueObject):
    """
    Value object representing a valid domain name.
    
    Validates domain names according to RFC 1123 specifications:
    - Total length up to 253 characters
    - Each label (part between dots) can be 1-63 characters
    - Can contain letters, digits, and hyphens
    - Hyphens cannot be at the beginning or end of a label
    - Must have at least one TLD with minimum 2 characters
    """

    value: str

    @override
    def _validate(self) -> None:
        """Validate that the domain name format is correct."""
        # Check if empty or whitespace only
        if not self.value or self.value.isspace():
            msg = "Domain name cannot be empty"
            raise InvalidDomainNameError(msg)

        # Check total length
        if len(self.value) > MAX_DOMAIN_LENGTH:
            msg = (
                f"Domain name too long: {len(self.value)} characters "
                f"(maximum {MAX_DOMAIN_LENGTH})"
            )
            raise InvalidDomainNameError(msg)

        # Convert to lowercase for validation (domain names are case-insensitive)
        lower_value: str = self.value.lower()

        # Check regex pattern
        if not DOMAIN_NAME_REGEX.fullmatch(lower_value):
            raise InvalidDomainNameError(
                f"Invalid domain name format: {self.value}. "
                "Domain must contain at least one dot and valid TLD"
            )

        # Additional validation: check each label
        labels = lower_value.split('.')

        # Check minimum TLD length
        tld = labels[-1]
        if len(tld) < 2:
            raise InvalidDomainNameError(
                f"Invalid domain name: TLD '{tld}' must be at least 2 characters"
            )

        # Validate each label
        for i, label in enumerate(labels):
            # Check label length
            if len(label) > 63:
                raise InvalidDomainNameError(
                    f"Invalid domain name: label '{label}' exceeds 63 characters"
                )

            # Check that label doesn't start or end with hyphen
            if label.startswith('-') or label.endswith('-'):
                raise InvalidDomainNameError(
                    f"Invalid domain name: label '{label}' cannot start or end with hyphen"
                )

    @override
    def __str__(self) -> str:
        """Return the domain name as a string."""
        return self.value

    @property
    def labels(self) -> list[str]:
        """Get all domain labels (parts separated by dots)."""
        return self.value.lower().split('.')

    @property
    def tld(self) -> str:
        """Get the top-level domain (TLD)."""
        return self.labels[-1]

    @property
    def root_domain(self) -> str:
        """Get the root domain (last two labels)."""
        if len(self.labels) >= 2:
            return '.'.join(self.labels[-2:])
        return self.value

    @property
    def is_subdomain(self) -> bool:
        """Check if this is a subdomain (has more than 2 labels)."""
        return len(self.labels) > 2



