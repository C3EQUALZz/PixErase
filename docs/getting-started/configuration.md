# Configuration

The PixErase follows the **Twelve-Factor App** methodology, using environment variables for configuration to ensure
flexibility and security.

## Configuration File

- **Backend Configuration Location**: `backend/src/pix_erase/setup/config`
- **Sample**: `.env.dist`

## Environment Variables

Key variables defined in `.env.dist` are organized by component:

### PostgreSQL Database

| Variable            | Description                | Default               |
|---------------------|----------------------------|-----------------------|
| `POSTGRES_HOST`     | PostgreSQL server hostname | `db`                  |
| `POSTGRES_USER`     | PostgreSQL username        | `postgres`            |
| `POSTGRES_PASSWORD` | PostgreSQL password        | `postgres`            |
| `POSTGRES_DB`       | PostgreSQL database name   | `automatic-responses` |
| `POSTGRES_PORT`     | PostgreSQL server port     | `5432`                |
| `POSTGRES_DRIVER`   | SQLAlchemy async driver    | `asyncpg`             |

### Database Connection Pool

| Variable               | Description                                | Default |
|------------------------|--------------------------------------------|---------|
| `DB_POOL_PRE_PING`     | Enable connection health checks before use | `True`  |
| `DB_POOL_RECYCLE`      | Connection recycling interval (seconds)    | `3600`  |
| `DB_POOL_SIZE`         | Base number of connections in the pool     | `50`    |
| `DB_POOL_MAX_OVERFLOW` | Maximum overflow connections allowed       | `25`    |
| `DB_ECHO`              | Enable SQLAlchemy query logging            | `False` |
| `DB_AUTO_FLUSH`        | Automatically flush changes before queries | `False` |
| `DB_EXPIRE_ON_COMMIT`  | Expire objects after commit                | `False` |
| `DB_DEBUG`             | Enable SQLAlchemy debug mode               | `True`  |
| `DB_FUTURE`            | Use SQLAlchemy 2.0 style behavior          | `True`  |

### RabbitMQ Message Broker

| Variable                | Description                 | Default    |
|-------------------------|-----------------------------|------------|
| `RABBITMQ_HOST`         | RabbitMQ server hostname    | `rabbitmq` |
| `RABBITMQ_PORT`         | RabbitMQ AMQP port          | `5672`     |
| `RABBITMQ_UI_PORT`      | RabbitMQ management UI port | `15672`    |
| `RABBITMQ_DEFAULT_USER` | RabbitMQ default username   | `guest`    |
| `RABBITMQ_DEFAULT_PASS` | RabbitMQ default password   | `guest`    |

### Uvicorn Server

| Variable       | Description                 | Default   |
|----------------|-----------------------------|-----------|
| `UVICORN_HOST` | Uvicorn server bind address | `0.0.0.0` |
| `UVICORN_PORT` | Uvicorn server port         | `8080`    |

### Redis Cache & Queue

| Variable                | Description                          | Default               |
|-------------------------|--------------------------------------|-----------------------|
| `REDIS_HOST`            | Redis server hostname                | `redis`               |
| `REDIS_PASSWORD`        | Redis default password               | `default`             |
| `REDIS_USER`            | Redis application user               | `automatic-responses` |
| `REDIS_USER_PASSWORD`   | Redis application user password      | `default`             |
| `REDIS_PORT`            | Redis server port                    | `6379`                |
| `REDIS_CACHE_DB`        | Redis database number for caching    | `0`                   |
| `REDIS_WORKER_DB`       | Redis database number for task queue | `1`                   |
| `REDIS_MAX_CONNECTIONS` | Maximum Redis connection pool size   | `20`                  |

### Security & Authentication

| Variable                    | Description                                 | Default                                          |
|-----------------------------|---------------------------------------------|--------------------------------------------------|
| `JWT_SECRET`                | Secret key for JWT token signing            | `REPLACE_THIS_WITH_YOUR_OWN_SECRET_VALUE`        |
| `JWT_ALGORITHM`             | JWT signing algorithm                       | `HS256`                                          |
| `PEPPER`                    | Password hashing pepper (additional secret) | `REPLACE_THIS_WITH_YOUR_OWN_SECRET_PEPPER_VALUE` |
| `SESSION_TTL_MIN`           | Session expiration time in minutes          | `5`                                              |
| `SESSION_REFRESH_THRESHOLD` | Session refresh threshold (ratio of TTL)    | `0.2`                                            |
| `SECURE`                    | Enable secure cookie flag (HTTPS only)      | `0`                                              |

### MinIO / S3 Object Storage

| Variable              | Description                       | Default        |
|-----------------------|-----------------------------------|----------------|
| `MINIO_HOST`          | MinIO server hostname             | `minio`        |
| `MINIO_PORT`          | MinIO S3 API port                 | `9000`         |
| `MINIO_UI_PORT`       | MinIO web UI port                 | `9001`         |
| `MINIO_ROOT_USER`     | MinIO root/admin username         | `minioadmin`   |
| `MINIO_ROOT_PASSWORD` | MinIO root/admin password         | `2eG1~B/j{70d` |
| `MINIO_IMAGES_BUCKET` | S3 bucket name for storing images | `images`       |

### Observability Stack

#### Grafana (Visualization & Dashboards)

| Variable           | Description            | Default |
|--------------------|------------------------|---------|
| `GRAFANA_PORT`     | Grafana web UI port    | `3000`  |
| `GRAFANA_USER`     | Grafana admin username | `admin` |
| `GRAFANA_PASSWORD` | Grafana admin password | `admin` |

#### Loki (Log Aggregation)

| Variable    | Description                       | Default |
|-------------|-----------------------------------|---------|
| `LOKI_PORT` | Loki log aggregation service port | `3100`  |

#### Vector (Log Router & Metrics)

| Variable      | Description                    | Default |
|---------------|--------------------------------|---------|
| `VECTOR_PORT` | Vector log router/metrics port | `8383`  |

#### Tempo (Distributed Tracing)

| Variable          | Description                         | Default     |
|-------------------|-------------------------------------|-------------|
| `TEMPO_HOST`      | Tempo distributed tracing hostname  | `localhost` |
| `TEMPO_PORT`      | Tempo HTTP API port                 | `3200`      |
| `TEMPO_GRPC_PORT` | Tempo gRPC endpoint port for traces | `4317`      |

#### Prometheus (Metrics Collection)

| Variable          | Description                        | Default |
|-------------------|------------------------------------|---------|
| `PROMETHEUS_PORT` | Prometheus metrics collection port | `9090`  |