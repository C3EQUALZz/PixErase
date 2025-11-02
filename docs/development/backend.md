# Backend Development

This guide covers the prerequisites and installation steps for backend of the PixErase.

## Prerequisites

- **Python**: >= 3.12
- **Docker**: For containerized deployment
- **Git**: For cloning the repository
- **Just**: Task runner

## Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/C3EQUALZz/PixErase
   cd PixErase/backend
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies: Use the provided just command to bootstrap the environment**:

   ```bash
   just bootstrap
   ```

   This copies .env.dist to .env, installs dependencies, and sets up pre-commit hooks.

4. **Docker Setup: To run the infrastructure with Docker**:

   ```bash
   just up-dev
   ```

   This starts all services defined in docker-compose.dev.yaml, including the API, database, broker.

5. **Scheduler Setup**:

    Open new window in terminal and run scheduler using this command: 
    
    ```bash
    taskiq scheduler pix_erase.scheduler:create_scheduler_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
    ```

6. **Worker Setup**:

    To run worker use this command:

    ```bash
    taskiq worker --ack-type when_saved pix_erase.worker:create_worker_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
    ```

7. **API Setup**
    
    To run api use this command:
    
    ```bash
    uvicorn --factory src.pix_erase.web:create_fastapi_app --port 8080
    ```

8. **Database Migration**
    
    Run migration using this command:
    
    ```bash
    alembic upgrade head
    ```

> [!NOTE]
> Super Admin in System is provided here:
> email: `admin@pixerase.com`
> password: `admin12345`

> [!NOTE]
> `Swagger`: http://localhost:8080