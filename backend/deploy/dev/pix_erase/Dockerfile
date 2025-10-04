FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

COPY ./pyproject.toml ./alembic.ini ./deploy/dev/pix_erase/api_entrypoint.sh ./deploy/dev/pix_erase/worker_entrypoint.sh ./
COPY ./src ./src

RUN uv pip install --system --no-cache --target dependencies "."


FROM python:3.12-slim AS production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

RUN apt-get update && apt-get install -y curl

COPY --from=builder /app/ ./