# Architecture Overview

The PixErase is built using **Clean Architecture** principles, ensuring a modular, testable, and maintainable codebase. This section provides an overview of the architectural design.

## Project Structure

The codebase is organized as follows:

- **`src/pix_erase/`**: Core application code
  - **`application/`**: Business logic (interactors)
  - **`entities/`**: Business models and value objects
  - **`infrastructure/`**: External integrations (e.g., database, observability)
  - **`presentation/`**: API endpoints and routing
  - **`setup/`**: Application configuration and IoC config
  - **`web.py`**: API entry point
  - **`worker.py`**: Worker entry point
  - **`scheduler.py`**: Scheduler entry point
- **`tests/`**: Unit and integration tests
- **`deploy/`**: Deployment configurations (Docker, Nginx, Grafana, etc.)
- **Configuration**: `.env.dist`, `pyproject.toml`, `alembic.ini`

## Key Components

- **FastAPI**: Powers the RESTful API.
- **SQLAlchemy/Alembic**: Manages database interactions and migrations.
- **TaskIQ**: Powers the scheduling and async background processing.
- **Dishka**: Handles dependency injection.
- **Observability**: Integrates Prometheus, Grafana, Loki, and Tempo for monitoring.
- **CI/CD**: GitHub Actions for testing, building, and deployment.

## Layers

The application follows Clean Architecture with two primary layers:

1. **Inner Layer**: Business logic (`src/pix_erase/application`, `src/pix_erase/entities`)

   - Independent of external tools.
   - Uses Python standard library only.
   - Communicates via interfaces.

2. **External Layer**: Tools and integrations (`src/pix_erase/infrastructure`, `src/pix_erase/presentation`)
   - Includes database, HTTP server, and observability tools.
   - Interacts with the inner layer through interfaces.

Learn more in the [Clean Architecture](clean-architecture.md) section.