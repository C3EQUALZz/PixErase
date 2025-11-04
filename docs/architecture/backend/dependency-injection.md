# Dependency Injection

The PixErase uses the **Dishka** framework for **dependency injection** (DI), ensuring that business logic remains independent of external dependencies.

## Why Dependency Injection?

- **Decoupling**: Business logic doesn’t directly reference databases, servers, or other tools.
- **Testability**: Dependencies can be mocked during testing.
- **Flexibility**: Swap implementations (e.g., change database adapters) without modifying use cases.

## Implementation

- **Framework**: Dishka (`src/pix_erase/setup/ioc.py`, `src/pix_erase/setup/bootstrap.py`)
- **Entry Point**: `src/pix_erase/web.py` initializes the application and injects dependencies.
- **Usage**: Dependencies are injected into use cases and routers (e.g., `UserCommandGateway`, `Transaction`).

## Configuration

Dependencies are defined in src/pix_erase/setup/ioc.py and wired in src/pix_erase/setup/bootstrap.py. For example:

- Database adapters (src/pix_erase/infrastructure/persistence/adapters).
- HTTP routers (src/pix_erase/presentation/http/v1/routes).

## Benefits

- Modularity: Change database or server implementations without touching business logic.
- Testability: Mock dependencies in unit tests (see tests/unit/application/conftest.py).
- Maintainability: Clear separation of concerns.

See the section for how DI fits into the broader architecture.