#!/bin/sh
set -e

echo 'Running alembic migrations...'
python -m alembic upgrade head
echo 'Starting Uvicorn...'
python -m uvicorn --factory src.pix_erase.web:create_fastapi_app --host ${UVICORN_HOST} --port ${UVICORN_PORT} --loop uvloop --workers 1