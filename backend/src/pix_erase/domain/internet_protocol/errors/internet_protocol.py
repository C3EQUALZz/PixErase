from pix_erase.domain.common.errors.base import DomainError, DomainFieldError


class InternetProtocolError(DomainError):
    """Base error for internet protocol related operations."""
    pass


class InvalidIPAddressError(InternetProtocolError):
    """Raised when an IP address format is invalid."""
    pass


class InvalidDomainNameError(DomainFieldError):
    """Raised when a domain name format is invalid."""
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


class IPInfoConnectionError(InternetProtocolError):
    """Raised when connection to IP information service fails."""
    pass


class IPInfoServiceError(InternetProtocolError):
    """Raised when IP information service returns an error."""
    pass


class IPInfoNotFoundError(InternetProtocolError):
    """Raised when IP information is not found."""
    pass


class PortScanError(InternetProtocolError):
    """Base error for port scanning operations."""
    pass


class PortScanTimeoutError(PortScanError):
    """Raised when port scan operation times out."""
    pass


class PortScanPermissionError(PortScanError):
    """Raised when port scan requires elevated permissions."""
    pass


class PortScanNetworkError(PortScanError):
    """Raised when a network error occurs during port scanning."""
    pass


class PortScanConnectionError(PortScanError):
    """Raised when connection to target fails during port scanning."""
    pass


class InvalidPortRangeError(DomainFieldError):
    """Raised when port range is invalid."""
    pass


class PortScanCancelledError(PortScanError):
    """Raised when port scan is cancelled."""
    pass


class BadPortRangeError(DomainFieldError):
    ...


class BadPortError(DomainFieldError):
    ...
