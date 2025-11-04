from typing import override

from bazario.asyncio import NotificationHandler

from pix_erase.domain.user.events import UserCreatedEvent


class CollectsStatisticsUserCreated(NotificationHandler[UserCreatedEvent]):
    def __init__(self) -> None: ...

    @override
    async def handle(self, notification: UserCreatedEvent) -> None: ...
