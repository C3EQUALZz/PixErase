#!/bin/sh
set -e

echo 'Running taskiq scheduler...'
taskiq scheduler pix_erase.scheduler:create_scheduler_taskiq_app -fsd -tp **/tasks/*.py
