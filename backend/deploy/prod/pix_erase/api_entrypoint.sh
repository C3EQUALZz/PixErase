#!/bin/sh
set -e

echo 'Running alembic migrations...'
python -m alembic upgrade head
echo 'Starting Uvicorn...'
python -Om src.pix_erase.web