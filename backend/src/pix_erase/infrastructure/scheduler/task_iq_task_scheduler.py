import logging
from datetime import datetime
from typing import Final, Any, Mapping

from redis.asyncio import Redis
from taskiq import AsyncBroker, ScheduleSource
from taskiq.depends.progress_tracker import TaskProgress, TaskState
from typing_extensions import override

from pix_erase.application.common.ports.scheduler.payloads.base import TaskPayload
from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskKey, TaskInfo, TaskInfoStatus
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler

logger: Final[logging.Logger] = logging.getLogger(__name__)


class TaskIQTaskScheduler(TaskScheduler):
    def __init__(
            self,
            broker: AsyncBroker,
            schedule_source: ScheduleSource,
            redis: Redis
    ) -> None:
        self._broker: Final[AsyncBroker] = broker
        self._schedule_source: Final[ScheduleSource] = schedule_source
        self._redis: Final[Redis] = redis

    @override
    async def schedule_by_time(
            self,
            task_id: TaskID,
            payload: TaskPayload,
            run_at: datetime
    ) -> None:
        task_name = task_id.split(":")[0]
        if task := self._broker.get_all_tasks().get(task_name):
            schedule = await task.schedule_by_time(
                self._schedule_source,
                run_at,
                payload
            )
            logger.debug("Schedule task %s at %s", task_id, run_at)
            await self._redis.set(task_id, schedule.schedule_id, ex=300)
            return

        raise ValueError(f"No task registered for {task_name}")

    @override
    async def unschedule(self, task_id: TaskID) -> None:
        schedule_id = await self._redis.get(task_id)
        if schedule_id:
            await self._schedule_source.delete_schedule(schedule_id)
            await self._redis.delete(task_id)
            logger.debug("Unschedule task %s", task_id)

    @override
    async def read_task_info(self, task_id: TaskID) -> TaskInfo | None:
        schedule_id = await self._redis.get(task_id)

        if not schedule_id:
            return None

        is_ready: bool = await self._broker.result_backend.is_result_ready(schedule_id)

        if not is_ready:
            return TaskInfo(
                task_id=task_id,
                status=TaskInfoStatus.PROCESSING,
                description="Processing task"
            )

        progress: TaskProgress[str] = await self._broker.result_backend.get_progress(schedule_id)

        map_with_task_iq_progress_and_our: Mapping[TaskState, TaskInfoStatus] = {
            TaskState.STARTED: TaskInfoStatus.STARTED,
            TaskState.FAILURE: TaskInfoStatus.FAILURE,
            TaskState.SUCCESS: TaskInfoStatus.SUCCESS,
            TaskState.RETRY: TaskInfoStatus.RETRYING
        }

        return TaskInfo(
            task_id=task_id,
            status=map_with_task_iq_progress_and_our.get(progress.state),
            description=progress.meta,
        )

    @override
    def make_task_id(self, key: TaskKey, value: Any) -> TaskID:
        return TaskID(f"{key}:{value}")
