from datetime import datetime
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator, model_validator


class PortScanRequestSchema(BaseModel):
    """Request schema for single port scan."""

    model_config = ConfigDict(frozen=True)

    target: Annotated[IPvAnyAddress, Field(description="Target IP address or hostname", examples=["192.168.1.1"])]
    port: Annotated[int, Field(ge=1, le=65535, description="Port number to scan", examples=[80])]
    timeout: Annotated[float, Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])]

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str) -> str:
        if not v or not v.strip():
            msg = "Target cannot be empty"
            raise ValueError(msg)
        return v.strip()


class PortScanResponse(BaseModel):
    """Response schema for single port scan."""

    model_config = ConfigDict(frozen=True)

    port: Annotated[int, Field(ge=1, le=65535, description="Port number to scan", examples=[80])]
    status: Annotated[Literal["open", "closed"], Field(examples=["open", "closed"], description="Status of port")]
    response_time: float | None = None
    service: str | None = None
    error_message: str | None = None
    scanned_at: datetime | None = None


class PortScanMultipleRequest(BaseModel):
    """Request schema for multiple ports scan."""

    model_config = ConfigDict(frozen=True)

    target: Annotated[IPvAnyAddress, Field(description="Target IP address or hostname", examples=["192.168.1.1"])]
    ports: Annotated[list[int], Field(description="List of ports to scan", examples=[[80, 443, 22], [5432, 5431]])]
    timeout: Annotated[float, Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])]
    max_concurrent: Annotated[
        int, Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    ]

    @field_validator("ports")
    @classmethod
    def validate_ports(cls, v: list[int]) -> list[int]:
        for port in v:
            if not (1 <= port <= 65535):  # noqa: PLR2004
                msg = f"Port {port} must be between 1 and 65535"
                raise ValueError(msg)
        return v


class PortScanRangeRequest(BaseModel):
    """Request schema for port range scan."""

    model_config = ConfigDict(frozen=True)

    target: Annotated[IPvAnyAddress, Field(description="Target IP address", examples=["192.168.1.1"])]
    start_port: Annotated[int, Field(ge=1, le=65535, description="Start port number", examples=[1])]
    end_port: Annotated[int, Field(ge=1, le=65535, description="End port number", examples=[1000])]
    timeout: Annotated[float, Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])]
    max_concurrent: Annotated[
        int, Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    ]

    @model_validator(mode="after")
    def validate_port_range(self) -> Self:
        if self.end_port < self.start_port:
            msg = "End port must be greater than or equal to start port"
            raise ValueError(msg)
        return self


class PortScanCommonRequest(BaseModel):
    """Request schema for common ports scan."""

    model_config = ConfigDict(frozen=True)

    target: Annotated[IPvAnyAddress, Field(description="Target IP address or hostname", examples=["192.168.1.1"])]
    timeout: Annotated[float, Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])]
    max_concurrent: Annotated[
        int, Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    ]


class PortScanResultResponseSchema(BaseModel):
    """Response schema for individual port scan result."""

    model_config = ConfigDict(frozen=True)

    port: Annotated[int, Field(description="Port number", examples=[80, 443, 5432], ge=1, le=65535)]
    status: Annotated[Literal["open", "closed"], Field(examples=["open", "closed"], description="Status of port")]
    response_time: Annotated[float | None, Field(default=None, description="Response time in seconds")]
    service: str | None = None
    error_message: str | None = None
    scanned_at: datetime | None = None


class PortScanSummaryResponse(BaseModel):
    """Response schema for port scan summary."""

    model_config = ConfigDict(frozen=True)

    target: IPvAnyAddress
    port_range: str
    total_ports: Annotated[int, Field(ge=0, description="Total number of ports")]
    open_ports: Annotated[int, Field(ge=0, description="Total number of open ports")]
    closed_ports: Annotated[int, Field(ge=0, description="Total number of closed ports")]
    filtered_ports: Annotated[int, Field(ge=0, description="Total number of filtered ports")]
    scan_duration: Annotated[float, Field(ge=0, description="Total duration in seconds")]
    started_at: datetime
    completed_at: datetime
    success_rate: Annotated[float, Field(ge=0, description="Success rate")]
    results: Annotated[list[PortScanResultResponseSchema], Field(description="List of port-scan results")]
