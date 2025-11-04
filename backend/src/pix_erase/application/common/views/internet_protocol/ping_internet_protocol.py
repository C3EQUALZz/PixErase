from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PingInternetProtocolView:
    """
    View for ping internet protocol response.

    This view represents the response data for ping operations
    that will be returned to the client.
    """

    success: bool
    response_time_ms: float | None = None
    error_message: str | None = None
    ttl: int | None = None
    packet_size: int | None = None
