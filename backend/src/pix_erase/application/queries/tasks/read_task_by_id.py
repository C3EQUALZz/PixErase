import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskInfo
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.tasks.read_task_by_id import ReadTaskByIDView
from pix_erase.application.errors.task import TaskNotFoundError

if TYPE_CHECKING:
    from pix_erase.domain.user.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadTaskByIDQuery:
    task_id: str


@final
class ReadTaskByIDQueryHandler:
    """
    - Opens to everyone.
    - Get tasks by id from cache.
    """

    def __init__(self, scheduler: TaskScheduler, current_user_service: CurrentUserService) -> None:
        self._scheduler: Final[TaskScheduler] = scheduler
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ReadTaskByIDQuery) -> ReadTaskByIDView:
        logger.info(
            "Started reading task with id: %s",
            data.task_id,
        )

        _: User = await self._current_user_service.get_current_user()

        typed_task_id: TaskID = TaskID(data.task_id)

        task_info: TaskInfo | None = await self._scheduler.read_task_info(task_id=typed_task_id)

        if task_info is None:
            msg = f"task with id {data.task_id} not found"
            raise TaskNotFoundError(msg)

        return ReadTaskByIDView(
            status=task_info.status,
            description=task_info.description,
        )
