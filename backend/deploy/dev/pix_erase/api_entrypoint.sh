#!/bin/sh
set -e

echo 'Running alembic migrations...'
python -m alembic upgrade head
echo 'Starting Uvicorn...'
python -m pix_erase/web.py