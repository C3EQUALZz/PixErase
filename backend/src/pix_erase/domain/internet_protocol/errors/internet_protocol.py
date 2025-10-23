from pix_erase.domain.common.errors.base import DomainError, DomainFieldError


class InternetProtocolError(DomainError):
    """Base error for internet protocol related operations."""
    pass


class InvalidIPAddressError(InternetProtocolError):
    """Raised when an IP address format is invalid."""
    pass


class InvalidPingResultError(InternetProtocolError):
    """Raised when ping result data is invalid."""
    pass


class PingTimeoutError(InternetProtocolError):
    """Raised when a ping operation times out."""
    pass


class PingDestinationUnreachableError(InternetProtocolError):
    """Raised when ping destination is unreachable."""
    pass


class PingTimeExceededError(InternetProtocolError):
    """Raised when ping time exceeded (TTL expired)."""
    pass


class PingPermissionError(InternetProtocolError):
    """Raised when ping operation requires elevated permissions."""
    pass


class PingNetworkError(InternetProtocolError):
    """Raised when a network error occurs during ping."""
    pass


class BadTimeOutError(DomainFieldError):
    ...


class BadPackageSizeError(DomainFieldError):
    ...


class BadTimeToLiveError(DomainFieldError):
    ...

