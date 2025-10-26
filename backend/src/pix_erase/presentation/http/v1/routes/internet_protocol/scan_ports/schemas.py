from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PortScanRequestSchema(BaseModel):
    """Request schema for single port scan."""
    
    target: str = Field(..., description="Target IP address or hostname", examples=["192.168.1.1"])
    port: int = Field(..., ge=1, le=65535, description="Port number to scan", examples=[80])
    timeout: float = Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])
    
    @field_validator('target')
    def validate_target(cls, v):
        if not v or not v.strip():
            raise ValueError("Target cannot be empty")
        return v.strip()


class PortScanResponse(BaseModel):
    """Response schema for single port scan."""
    
    port: int
    status: str
    response_time: float | None = None
    service: str | None = None
    error_message: str | None = None
    scanned_at: datetime | None = None


class PortScanMultipleRequest(BaseModel):
    """Request schema for multiple ports scan."""
    
    target: str = Field(..., description="Target IP address or hostname", examples=["192.168.1.1"])
    ports: list[int] = Field(..., description="List of ports to scan", examples=[80, 443, 22])
    timeout: float = Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])
    max_concurrent: int = Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    
    @field_validator('target')
    def validate_target(cls, v):
        if not v or not v.strip():
            raise ValueError("Target cannot be empty")
        return v.strip()
    
    @field_validator('ports')
    def validate_ports(cls, v):
        for port in v:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} must be between 1 and 65535")
        return v


class PortScanRangeRequest(BaseModel):
    """Request schema for port range scan."""
    
    target: str = Field(..., description="Target IP address or hostname", examples=["192.168.1.1"])
    start_port: int = Field(..., ge=1, le=65535, description="Start port number", examples=[1])
    end_port: int = Field(..., ge=1, le=65535, description="End port number", examples=[1000])
    timeout: float = Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])
    max_concurrent: int = Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    
    @field_validator('target')
    def validate_target(cls, v):
        if not v or not v.strip():
            raise ValueError("Target cannot be empty")
        return v.strip()
    
    @field_validator('end_port')
    def validate_port_range(cls, v, values):
        if 'start_port' in values and v < values['start_port']:
            raise ValueError("End port must be greater than or equal to start port")
        return v


class PortScanCommonRequest(BaseModel):
    """Request schema for common ports scan."""
    
    target: str = Field(..., description="Target IP address or hostname", examples=["192.168.1.1"])
    timeout: float = Field(default=1.0, ge=0.1, le=30.0, description="Timeout in seconds", examples=[1.0])
    max_concurrent: int = Field(default=100, ge=1, le=500, description="Maximum concurrent scans", examples=[100])
    
    @field_validator('target')
    def validate_target(cls, v):
        if not v or not v.strip():
            raise ValueError("Target cannot be empty")
        return v.strip()


class PortScanResultResponseSchema(BaseModel):
    """Response schema for individual port scan result."""
    
    port: int
    status: str
    response_time: float | None = None
    service: str | None = None
    error_message: str | None = None
    scanned_at: datetime | None = None


class PortScanSummaryResponse(BaseModel):
    """Response schema for port scan summary."""
    
    target: str
    port_range: str
    total_ports: int
    open_ports: int
    closed_ports: int
    filtered_ports: int
    scan_duration: float
    started_at: datetime
    completed_at: datetime
    success_rate: float
    results: list[PortScanResultResponseSchema]


class PortScanCommonResponse(BaseModel):
    """Response schema for common ports scan."""
    
    target: str
    port_range: str
    total_ports: int
    open_ports: int
    closed_ports: int
    filtered_ports: int
    scan_duration: float
    started_at: datetime
    completed_at: datetime
    success_rate: float
    results: list[PortScanResultResponseSchema]



