import logging
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
    async def schedule(
            self,
            task_id: TaskID,
            payload: TaskPayload,
    ) -> None:
        task_name = task_id.split(":")[0]

        logger.debug("All tasks: %s", self._broker.get_all_tasks())

        if task := self._broker.get_all_tasks().get(task_name):
            await task.kicker().with_task_id(task_id).kiq(payload)
            logger.info("Schedule task at %s", task_id)
            return

        raise ValueError(f"No task registered for {task_name}")

    @override
    async def read_task_info(self, task_id: TaskID) -> TaskInfo | None:
        logger.info("Task id: %s", task_id)

        progress: TaskProgress[str] | None = await self._broker.result_backend.get_progress(task_id)

        if progress is None:
            return None

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
