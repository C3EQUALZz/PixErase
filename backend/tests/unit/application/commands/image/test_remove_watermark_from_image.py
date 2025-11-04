from unittest.mock import Mock
from uuid import uuid4

import pytest

from pix_erase.application.commands.image.remove_watermark_from_image import (
    RemoveWatermarkFromImageCommand,
    RemoveWatermarkFromImageCommandHandler,
)


@pytest.mark.asyncio
async def test_remove_watermark_noop(
    fake_current_user_service: Mock,
    fake_image_storage: Mock,
    fake_task_scheduler: Mock,
) -> None:
    # Handler currently only logs, ensure it doesn't raise
    sut = RemoveWatermarkFromImageCommandHandler(
        image_storage=fake_image_storage,
        task_scheduler=fake_task_scheduler,
        current_user_service=fake_current_user_service,
    )

    await sut(RemoveWatermarkFromImageCommand(image_id=uuid4(), use_ai=True))
