from abc import abstractmethod
from typing import Protocol

from pix_erase.domain.internet_protocol.values.domain_id import DomainID


class DomainIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> DomainID: ...
