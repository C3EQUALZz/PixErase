#!/bin/sh
set -e

echo 'Running taskiq tasks...'
python -m taskiq worker -fsd --ack-type when_saved pix_erase.worker:create_taskiq_app -tp pix_erase.infrastructure.task_manager.tasks