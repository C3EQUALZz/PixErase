from pix_erase.domain.common.errors.base import DomainFieldError


class EmptyPasswordWasProvidedError(DomainFieldError): ...


class WeakPasswordWasProvidedError(DomainFieldError): ...
