from typing import Annotated

from pydantic import BaseModel, networks, Field


class PingSchemaRequest(BaseModel):
    destination_address: networks.IPvAnyAddress
    timeout: Annotated[float, Field(default=4.0, description="Ping timeout", gt=0.0)]
    packet_size: Annotated[int, Field(default=56, description="Packet size for processing", ge=56)]
    ttl: Annotated[int | None, Field(default=None, description="time to live", ge=1)]


class PingSchemaResponse(BaseModel):
    success: Annotated[bool, Field(description="True if ping was successful")]
    response_time_ms: Annotated[float | None, Field(default=None, description="response time in milliseconds", ge=0.0)]
    error_message: Annotated[str | None, Field(default=None, description="Error message from server", min_length=1)]
    ttl: Annotated[int | None, Field(default=None, description="Time to live in seconds", ge=0)]
    packet_size: Annotated[int | None, Field(default=None, description="Packet size for processing", ge=0)]
