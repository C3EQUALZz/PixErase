from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class IPInfoView:
    """
    View for IP information response.

    This view represents the IP information data
    that will be returned to the client.
    """

    ip_address: str
    isp: str | None = None
    organization: str | None = None
    country: str | None = None
    region_name: str | None = None
    city: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    has_location: bool = False
    has_network_info: bool = False
    location_string: str = ""
    network_string: str = ""
