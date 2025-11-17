from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.phone_number.values.phone_id import PhoneID


class PhoneIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> PhoneID: ...
