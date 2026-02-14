from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ("destination_address", "timeout", "packet_size", "ttl")
    DESTINATION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    PACKET_SIZE_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    destination_address: str
    timeout: float
    packet_size: int
    ttl: int
    def __init__(self, destination_address: _Optional[str] = ..., timeout: _Optional[float] = ..., packet_size: _Optional[int] = ..., ttl: _Optional[int] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("success", "response_time_ms", "error_message", "ttl", "packet_size")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    PACKET_SIZE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    response_time_ms: float
    error_message: str
    ttl: int
    packet_size: int
    def __init__(self, success: bool = ..., response_time_ms: _Optional[float] = ..., error_message: _Optional[str] = ..., ttl: _Optional[int] = ..., packet_size: _Optional[int] = ...) -> None: ...

class ReadIPInfoRequest(_message.Message):
    __slots__ = ("ip_address",)
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    def __init__(self, ip_address: _Optional[str] = ...) -> None: ...

class ReadIPInfoResponse(_message.Message):
    __slots__ = ("ip_address", "isp", "organization", "country", "region_name", "city", "zip_code", "latitude", "longitude", "has_location", "has_network_info", "location_string", "network_string")
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ISP_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    REGION_NAME_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    ZIP_CODE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    HAS_LOCATION_FIELD_NUMBER: _ClassVar[int]
    HAS_NETWORK_INFO_FIELD_NUMBER: _ClassVar[int]
    LOCATION_STRING_FIELD_NUMBER: _ClassVar[int]
    NETWORK_STRING_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    isp: str
    organization: str
    country: str
    region_name: str
    city: str
    zip_code: str
    latitude: float
    longitude: float
    has_location: bool
    has_network_info: bool
    location_string: str
    network_string: str
    def __init__(self, ip_address: _Optional[str] = ..., isp: _Optional[str] = ..., organization: _Optional[str] = ..., country: _Optional[str] = ..., region_name: _Optional[str] = ..., city: _Optional[str] = ..., zip_code: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., has_location: bool = ..., has_network_info: bool = ..., location_string: _Optional[str] = ..., network_string: _Optional[str] = ...) -> None: ...

class ScanPortRequest(_message.Message):
    __slots__ = ("target", "port", "timeout")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    target: str
    port: int
    timeout: float
    def __init__(self, target: _Optional[str] = ..., port: _Optional[int] = ..., timeout: _Optional[float] = ...) -> None: ...

class PortScanResultResponse(_message.Message):
    __slots__ = ("port", "status", "response_time", "service", "error_message", "scanned_at")
    PORT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SCANNED_AT_FIELD_NUMBER: _ClassVar[int]
    port: int
    status: str
    response_time: float
    service: str
    error_message: str
    scanned_at: str
    def __init__(self, port: _Optional[int] = ..., status: _Optional[str] = ..., response_time: _Optional[float] = ..., service: _Optional[str] = ..., error_message: _Optional[str] = ..., scanned_at: _Optional[str] = ...) -> None: ...

class ScanPortsRequest(_message.Message):
    __slots__ = ("target", "ports", "timeout", "max_concurrent")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_CONCURRENT_FIELD_NUMBER: _ClassVar[int]
    target: str
    ports: _containers.RepeatedScalarFieldContainer[int]
    timeout: float
    max_concurrent: int
    def __init__(self, target: _Optional[str] = ..., ports: _Optional[_Iterable[int]] = ..., timeout: _Optional[float] = ..., max_concurrent: _Optional[int] = ...) -> None: ...

class ScanPortsResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[PortScanResultResponse]
    def __init__(self, results: _Optional[_Iterable[_Union[PortScanResultResponse, _Mapping]]] = ...) -> None: ...

class ScanPortRangeRequest(_message.Message):
    __slots__ = ("target", "start_port", "end_port", "timeout", "max_concurrent")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    START_PORT_FIELD_NUMBER: _ClassVar[int]
    END_PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_CONCURRENT_FIELD_NUMBER: _ClassVar[int]
    target: str
    start_port: int
    end_port: int
    timeout: float
    max_concurrent: int
    def __init__(self, target: _Optional[str] = ..., start_port: _Optional[int] = ..., end_port: _Optional[int] = ..., timeout: _Optional[float] = ..., max_concurrent: _Optional[int] = ...) -> None: ...

class ScanCommonPortsRequest(_message.Message):
    __slots__ = ("target", "timeout", "max_concurrent")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    MAX_CONCURRENT_FIELD_NUMBER: _ClassVar[int]
    target: str
    timeout: float
    max_concurrent: int
    def __init__(self, target: _Optional[str] = ..., timeout: _Optional[float] = ..., max_concurrent: _Optional[int] = ...) -> None: ...

class PortScanSummaryResponse(_message.Message):
    __slots__ = ("target", "port_range", "total_ports", "open_ports", "closed_ports", "filtered_ports", "scan_duration", "started_at", "completed_at", "success_rate", "results")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PORTS_FIELD_NUMBER: _ClassVar[int]
    OPEN_PORTS_FIELD_NUMBER: _ClassVar[int]
    CLOSED_PORTS_FIELD_NUMBER: _ClassVar[int]
    FILTERED_PORTS_FIELD_NUMBER: _ClassVar[int]
    SCAN_DURATION_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    target: str
    port_range: str
    total_ports: int
    open_ports: int
    closed_ports: int
    filtered_ports: int
    scan_duration: float
    started_at: str
    completed_at: str
    success_rate: float
    results: _containers.RepeatedCompositeFieldContainer[PortScanResultResponse]
    def __init__(self, target: _Optional[str] = ..., port_range: _Optional[str] = ..., total_ports: _Optional[int] = ..., open_ports: _Optional[int] = ..., closed_ports: _Optional[int] = ..., filtered_ports: _Optional[int] = ..., scan_duration: _Optional[float] = ..., started_at: _Optional[str] = ..., completed_at: _Optional[str] = ..., success_rate: _Optional[float] = ..., results: _Optional[_Iterable[_Union[PortScanResultResponse, _Mapping]]] = ...) -> None: ...

class AnalyzeDomainRequest(_message.Message):
    __slots__ = ("domain", "timeout")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    domain: str
    timeout: float
    def __init__(self, domain: _Optional[str] = ..., timeout: _Optional[float] = ...) -> None: ...

class DnsRecordEntry(_message.Message):
    __slots__ = ("record_type", "values")
    RECORD_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    record_type: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, record_type: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class AnalyzeDomainResponse(_message.Message):
    __slots__ = ("domain_id", "domain_name", "dns_records", "subdomains", "title", "created_at", "updated_at")
    DOMAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    DNS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    SUBDOMAINS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    domain_id: str
    domain_name: str
    dns_records: _containers.RepeatedCompositeFieldContainer[DnsRecordEntry]
    subdomains: _containers.RepeatedScalarFieldContainer[str]
    title: str
    created_at: str
    updated_at: str
    def __init__(self, domain_id: _Optional[str] = ..., domain_name: _Optional[str] = ..., dns_records: _Optional[_Iterable[_Union[DnsRecordEntry, _Mapping]]] = ..., subdomains: _Optional[_Iterable[str]] = ..., title: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...
