from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.ports.scheduler.task_id import TaskID, TaskInfo, TaskInfoStatus
from pix_erase.application.common.ports.scheduler.task_scheduler import TaskScheduler
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.errors.task import TaskNotFoundError
from pix_erase.application.queries.tasks.read_task_by_id import (
    ReadTaskByIDQuery,
    ReadTaskByIDQueryHandler,
)


@pytest.mark.asyncio
async def test_read_task_by_id_success(
    fake_task_scheduler: TaskScheduler,
    fake_current_user_service: CurrentUserService,
) -> None:
    # Arrange
    task_id = TaskID("compare_images:abc-123")
    task_info = TaskInfo(status=TaskInfoStatus.STARTED, description="All good", task_id=task_id)
    fake_task_scheduler.read_task_info = AsyncMock(return_value=task_info)  # type: ignore[attr-defined]

    sut = ReadTaskByIDQueryHandler(scheduler=fake_task_scheduler, current_user_service=fake_current_user_service)

    # Act
    view = await sut(ReadTaskByIDQuery(task_id=str(task_id)))

    # Assert
    assert view.status == task_info.status
    assert view.description == task_info.description


@pytest.mark.asyncio
async def test_read_task_by_id_not_found(
    fake_task_scheduler: TaskScheduler,
    fake_current_user_service: CurrentUserService,
) -> None:
    # Arrange
    task_id = TaskID("compress_image:missing")
    fake_task_scheduler.read_task_info = AsyncMock(return_value=None)  # type: ignore[attr-defined]

    sut = ReadTaskByIDQueryHandler(scheduler=fake_task_scheduler, current_user_service=fake_current_user_service)

    # Act / Assert
    with pytest.raises(TaskNotFoundError):
        await sut(ReadTaskByIDQuery(task_id=str(task_id)))

