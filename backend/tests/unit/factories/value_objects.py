import uuid
from dataclasses import dataclass
from uuid import UUID

from pix_erase.domain.common.values.base import BaseValueObject
from pix_erase.domain.internet_protocol.values.domain_id import DomainID
from pix_erase.domain.internet_protocol.values.domain_name import DomainName
from pix_erase.domain.internet_protocol.values.ip_address import IPv4Address, IPv6Address
from pix_erase.domain.internet_protocol.values.packet_size import PacketSize
from pix_erase.domain.internet_protocol.values.ping_result import PingResult
from pix_erase.domain.internet_protocol.values.port import Port
from pix_erase.domain.internet_protocol.values.time_to_live import TimeToLive
from pix_erase.domain.internet_protocol.values.timeout import Timeout
from pix_erase.domain.user.values.hashed_password import HashedPassword
from pix_erase.domain.user.values.raw_password import RawPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_name import Username


@dataclass(frozen=True, slots=True, repr=True)
class SingleFieldVO(BaseValueObject):
    value: int

    def _validate(self) -> None: ...

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True, repr=True)
class MultiFieldVO(BaseValueObject):
    value1: int
    value2: str

    def _validate(self) -> None: ...

    def __str__(self) -> str:
        return str(self.value1) + str(self.value2)


def create_single_field_vo(value: int = 1) -> SingleFieldVO:
    return SingleFieldVO(value)


def create_multi_field_vo(value1: int = 1, value2: str = "Alice") -> MultiFieldVO:
    return MultiFieldVO(value1, value2)


def create_user_id(value: UUID | None = None) -> UserID:
    return UserID(value if value else uuid.uuid4())


def create_username(value: str = "Alice") -> Username:
    return Username(value)


def create_raw_password(value: str = "Good Password") -> RawPassword:
    return RawPassword(value)


def create_password_hash(value: bytes = b"password_hash") -> HashedPassword:
    return HashedPassword(value)


def create_user_email(value: str = "alice@example.com") -> UserEmail:
    return UserEmail(value)


def create_ipv4_address(value: str = "192.168.1.1") -> IPv4Address:
    return IPv4Address(value=value)


def create_ipv6_address(value: str = "2001:0db8:85a3:0000:0000:8a2e:0370:7334") -> IPv6Address:
    return IPv6Address(value=value)


def create_domain_name(value: str = "example.com") -> DomainName:
    return DomainName(value=value)


def create_port(value: int = 80) -> Port:
    return Port(value=value)


def create_timeout(value: float = 4.0) -> Timeout:
    return Timeout(value=value)


def create_packet_size(value: int = 56) -> PacketSize:
    return PacketSize(value=value)


def create_time_to_live(value: int = 64) -> TimeToLive:
    return TimeToLive(value=value)


def create_ping_result(
    success: bool | None = None,
    response_time_ms: float | None = None,
    error_message: str | None = None,
    ttl: int | None = 64,
    packet_size: int | None = 56,
) -> PingResult:
    if success is None:
        success = True
    # Для successful ping нужен response_time_ms, для failed - не должен быть установлен
    if success and response_time_ms is None:
        response_time_ms = 10.5
    elif not success:
        response_time_ms = None

    return PingResult(
        success=success,
        response_time_ms=response_time_ms,
        error_message=error_message,
        ttl=ttl,
        packet_size=packet_size,
    )


def create_domain_id(value: UUID | None = None) -> DomainID:
    return DomainID(value if value else uuid.uuid4())
