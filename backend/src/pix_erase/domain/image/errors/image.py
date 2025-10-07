from pix_erase.domain.common.errors.base import DomainFieldError, DomainError


class BadImageSizeError(DomainFieldError):
    ...


class BadImageNameError(DomainFieldError):
    ...


class BadImageScaleError(DomainError):
    ...


class UnknownImageUpscalerError(DomainError):
    ...


class BadImageUpscaleAlgorithmError(DomainError):
    ...
