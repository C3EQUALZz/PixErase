from pix_erase.domain.common.errors.base import DomainFieldError


class EmptyRegionOfPhoneNumberError(DomainFieldError): ...


class InvalidRegionOfPhoneNumberLengthError(DomainFieldError): ...
