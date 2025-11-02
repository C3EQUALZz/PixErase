# **Contributing**

Contributions to the PixErase are welcome! This guide outlines how to contribute.

> [!IMPORTANT]
> Make sure that `just`, `docker` is installed on your system.

## **Getting Started with backend**

1. **Fork the Repository**:
   Fork [C3EQUALZz/PixErase](https://github.com/C3EQUALZz/PixErase).

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/<your_username>/pure-architecture-fastapi
   cd PixErase/backend
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Set Up Development**:
   ```bash
   just bootstrap
   ```

### Making Changes

#### Create a Branch:

```bash
git checkout -b feature/your-feature
```

#### Follow Coding Standards:

- Use Ruff for linting (`just lint`).
- Run static analysis (`just static`).
- Write tests (`just test`).

#### Commit Messages: Use conventional commits (enforced by conventional-pre-commit):

- **Example**: `feat: add new endpoint`
- **Types**: `feat`, `fix`, `docs`, `chore`, `style`, `refactor`, `test`, `build`.

#### Run Pre-Commit Hooks:

```bash
pre-commit run --all-files
```

### Submitting Changes

#### Push Changes:

```bash
git push origin feature/your-feature
```

#### Create a Pull Request:

- Target the develop branch.
- Describe the changes and reference any issues.

### CI Checks: The PR will trigger pr-tests.yaml to run tests and linters. Ensure all checks pass.

#### Code Review

- Respond to feedback promptly.
- Make necessary changes and push updates to the same branch.

#### Issues

Report bugs or suggest features via GitHub Issues.

#### Contact

- **Author**: Danil Kovalev ([GitHub](https://github.com/C3EQUALZz))

Thank you for contributing!