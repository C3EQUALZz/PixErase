#!/bin/sh
set -e

echo 'Running taskiq tasks...'
python -m taskiq worker -fsd --ack-type when_saved automatic_responses.worker:create_taskiq_app -tp automatic_responses.infrastructure.tasks