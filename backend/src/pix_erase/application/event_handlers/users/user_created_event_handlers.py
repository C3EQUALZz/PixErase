from bazario.asyncio import NotificationHandler
from typing_extensions import override

from pix_erase.domain.user.events import UserCreatedEvent


class CollectsStatisticsUserCreated(NotificationHandler[UserCreatedEvent]):
    def __init__(self) -> None:
        ...

    @override
    async def handle(self, notification: UserCreatedEvent) -> None:
        ...
