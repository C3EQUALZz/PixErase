from typing import Protocol, Any
from datetime import datetime
from abc import abstractmethod
from pix_erase.application.common.ports.scheduler.payloads.base import TaskPayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskKey, TaskInfo


class TaskScheduler(Protocol):
    @abstractmethod
    async def schedule_by_time(
            self,
            task_id: TaskID,
            payload: TaskPayload,
            run_at: datetime,
    ) -> None:
        ...

    @abstractmethod
    async def unschedule(
            self,
            task_id: TaskID
    ) -> None:
        ...

    @abstractmethod
    def make_task_id(self, key: TaskKey, value: Any) -> TaskID:
        ...

    @abstractmethod
    async def read_task_info(self, task_id: TaskID) -> TaskInfo | None:
        ...
