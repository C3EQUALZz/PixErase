from pydantic import BaseModel, networks


class ReadIPInfoSchemaRequest(BaseModel):
    destination_address: networks.IPvAnyAddress


class ReadIPInfoSchemaResponse(BaseModel):
    ip_address: networks.IPvAnyAddress
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
