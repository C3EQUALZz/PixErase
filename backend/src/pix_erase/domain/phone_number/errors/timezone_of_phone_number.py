from pix_erase.domain.common.errors.base import DomainFieldError


class EmptyTimezoneOfPhoneNumberError(DomainFieldError): ...


class InvalidTimezoneOfPhoneNumberFormatError(DomainFieldError): ...
