# PixErase Backend

Backend part of the OSINT service for data processing.

## Implementation Principle

The project uses the `Clean Architecture` and `EDA` (Event-Driven Architecture) approaches.

## Dependencies

The following dependencies are used in the project, which are presented in [`pyproject.toml`](pyproject.toml)

## Deployment

> [!IMPORTANT]
> Make sure that `Docker` and `Docker Compose` are installed on your PC or server.

### Local Development

> [!IMPORTANT]
> [`just`](https://github.com/casey/just) is used for running and interacting with the project.
> All subsequent commands in this manual will use `just`.

#### Environment Variables Initialization

First, create a `.env` file by copying values from `.env.dist`.

> [!IMPORTANT]
> When running the application without `Docker`, all hosts should be changed to `localhost`.

#### Python Project Initialization

Create a `.venv` using `Python 3.12`.
After that, you need to install `uv` in this virtual environment using the command:

```bash
pip install uv
```

Now install the libraries and frameworks used in the project with the command:

```bash
uv install
```

#### Starting Infrastructure Dependencies

To start `RabbitMQ`, `PostgreSQL`, `MinIO`, and `Redis`, use the command:

```bash
just up-dev
```

> [!IMPORTANT]
> It is expected that `.env` has been created successfully beforehand.

#### Starting the Scheduler

To start the `worker`, use the command below:

```bash
taskiq worker --ack-type when_saved pix_erase.worker:create_worker_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
```

Now start the `scheduler` itself in a separate process:

```bash
taskiq scheduler pix_erase.scheduler:create_scheduler_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
```

> [!IMPORTANT]
> It is expected that `.env` has been created successfully beforehand.
> It is expected that infrastructure dependencies have already been started.

#### Running Migrations

```bash
alembic upgrade head
```

#### Starting the API

To start the `api`, use the command below:

```bash
uvicorn --factory src.pix_erase.web:create_fastapi_app --port 8080
```

> [!IMPORTANT]
> It is expected that `.env` has been created successfully beforehand.
> It is expected that infrastructure dependencies have already been started.
> It is expected that the `worker` has been started beforehand.

> [!NOTE]
> `Swagger` will be available at http://localhost:8080/api/docs

Super admin account credentials:

> email: `admin@pixerase.com`
> password: `admin12345`