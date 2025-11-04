from abc import abstractmethod
from typing import Any, Protocol

from pix_erase.application.common.ports.scheduler.payloads.base import TaskPayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskInfo, TaskKey


class TaskScheduler(Protocol):
    @abstractmethod
    async def schedule(
        self,
        task_id: TaskID,
        payload: TaskPayload,
    ) -> None: ...

    @abstractmethod
    def make_task_id(self, key: TaskKey, value: Any) -> TaskID: ...

    @abstractmethod
    async def read_task_info(self, task_id: TaskID) -> TaskInfo | None: ...
