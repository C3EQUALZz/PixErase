#!/bin/sh
set -e

echo 'Running taskiq scheduler...'
taskiq scheduler -fsd pix_erase.scheduler:create_scheduler_taskiq_app -tp pix_erase.infrastructure.task_manager.tasks
