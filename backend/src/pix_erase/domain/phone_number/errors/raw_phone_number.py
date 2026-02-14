from pix_erase.domain.common.errors.base import DomainFieldError


class EmptyRawPhoneNumberError(DomainFieldError): ...


class InvalidRawPhoneNumberFormatError(DomainFieldError): ...
