from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.phone_number.values import (
    OperatorOfPhoneNumber,
    RegionOfPhoneNumber,
    TimezoneOfPhoneNumber,
    TypeOfPhoneNumber,
)
from pix_erase.domain.phone_number.values.raw_phone_number import RawPhoneNumber


class PhoneInfoServicePort(Protocol):
    """
    Protocol for phone number information service implementations.

    This defines the interface for services that provide
    information about phone numbers, including type, operator, region, and timezone.
    """

    @abstractmethod
    def get_type_number(self, raw_phone_number: RawPhoneNumber) -> TypeOfPhoneNumber: ...

    @abstractmethod
    def get_operator(self, raw_phone_number: RawPhoneNumber) -> OperatorOfPhoneNumber: ...

    @abstractmethod
    def get_region(self, raw_phone_number: RawPhoneNumber) -> RegionOfPhoneNumber: ...

    @abstractmethod
    def get_timezone(self, raw_phone_number: RawPhoneNumber) -> TimezoneOfPhoneNumber: ...
