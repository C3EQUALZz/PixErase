from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from pix_erase.domain.common.events import BaseDomainEvent


class EventBus(Protocol):
    @abstractmethod
    async def publish(self, events: Iterable[BaseDomainEvent]) -> None:
        raise NotImplementedError
