#!/bin/sh
set -e

echo 'Running taskiq tasks...'
taskiq worker --ack-type when_saved pix_erase.worker:create_worker_taskiq_app -fsd -tp **/tasks/*.py
