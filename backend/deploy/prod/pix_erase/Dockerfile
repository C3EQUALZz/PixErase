FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY ./pyproject.toml ./uv.lock ./alembic.ini ./deploy/prod/pix_erase/api_entrypoint.sh ./deploy/prod/pix_erase/worker_entrypoint.sh ./deploy/prod/pix_erase/scheduler_entrypoint.sh ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY ./src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.12-slim-bookworm AS final

WORKDIR /app

ARG APP_UID=10001
ARG APP_GID=10001

ENV VIRTUAL_ENV="/app/.venv" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -g ${APP_GID} appgroup && \
    useradd -u ${APP_UID} -g ${APP_GID} -s /usr/sbin/nologin -M appuser

COPY --from=builder --chown=${APP_UID}:${APP_GID} /app/ ./

USER appuser