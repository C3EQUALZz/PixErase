from pix_erase.domain.common.errors.base import DomainError, DomainFieldError


class InternetProtocolError(DomainError):
    """Base error for internet protocol related operations."""


class InvalidIPAddressError(InternetProtocolError):
    """Raised when an IP address format is invalid."""


class InvalidDomainNameError(DomainFieldError):
    """Raised when a domain name format is invalid."""


class InvalidPingResultError(InternetProtocolError):
    """Raised when ping result data is invalid."""


class PingTimeoutError(InternetProtocolError):
    """Raised when a ping operation times out."""


class PingDestinationUnreachableError(InternetProtocolError):
    """Raised when ping destination is unreachable."""


class PingTimeExceededError(InternetProtocolError):
    """Raised when ping time exceeded (TTL expired)."""


class PingPermissionError(InternetProtocolError):
    """Raised when ping operation requires elevated permissions."""


class PingNetworkError(InternetProtocolError):
    """Raised when a network error occurs during ping."""


class BadTimeOutError(DomainFieldError): ...


class BadPackageSizeError(DomainFieldError): ...


class BadTimeToLiveError(DomainFieldError): ...


class IPInfoConnectionError(InternetProtocolError):
    """Raised when connection to IP information service fails."""


class IPInfoServiceError(InternetProtocolError):
    """Raised when IP information service returns an error."""


class IPInfoNotFoundError(InternetProtocolError):
    """Raised when IP information is not found."""


class PortScanError(InternetProtocolError):
    """Base error for port scanning operations."""


class PortScanTimeoutError(PortScanError):
    """Raised when port scan operation times out."""


class PortScanPermissionError(PortScanError):
    """Raised when port scan requires elevated permissions."""


class PortScanNetworkError(PortScanError):
    """Raised when a network error occurs during port scanning."""


class PortScanConnectionError(PortScanError):
    """Raised when connection to target fails during port scanning."""


class InvalidPortRangeError(DomainFieldError):
    """Raised when port range is invalid."""


class PortScanCancelledError(PortScanError):
    """Raised when port scan is cancelled."""


class BadPortRangeError(DomainFieldError): ...


class BadPortError(DomainFieldError): ...
