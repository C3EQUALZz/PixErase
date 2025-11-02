# Clean Architecture

The PixErase adheres to **Clean Architecture** principles, as outlined by Robert Martin (Uncle Bob). This approach ensures the codebase remains scalable, testable, and independent of external systems.

## Core Principles

- **Dependency Inversion**: Dependencies flow inward, isolating business logic from external tools.
- **Separation of Concerns**: Each layer has a distinct responsibility.
- **Testability**: Business logic is easily testable without external dependencies.
- **Extensibility**: New features or integrations can be added with minimal changes.

## Layers

Clean Architecture divides the application into layers:

### Entities (`src/pix_erase/domain`):

- Business models.
- Contain validation logic and value objects.
- Reusable across layers.

### Use Cases (`src/pix_erase/application`):

- Business logic organized by domain (e.g., `commands`, `queries`).
- Encapsulates operations like creating, updating, or querying users.
- Interacts with repositories via interfaces.

### Interface Adapters (`src/pix_erase/presentation`, `src/pix_erase/infrastructure`):

- Translates data between the inner layer and external systems.
- Includes HTTP routers (`presentation/http`) and database adapters (`infrastructure/persistence`).

### Frameworks and Drivers (`deploy`, external libraries):

- External tools like FastAPI, SQLAlchemy, and Docker.
- Configured to interact with the inner layers via adapters.

## Data Flow

A typical request flow:

```text
HTTP Request → Presentation (Router) → Interactor → Repository (Database) → Interactor → Presentation → HTTP Response`
```

## Benefits

- **Independence**: Business logic is decoupled from databases, servers, or frameworks.
- **Testability**: Use cases can be tested without mocking external systems.
- **Flexibility**: Swap out tools (e.g., replace PostgreSQL with MongoDB) by updating adapters.

See [Dependency Injection](dependency-injection.md) for how dependencies are managed.