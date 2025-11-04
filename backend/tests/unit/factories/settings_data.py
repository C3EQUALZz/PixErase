from typing import Literal, TypedDict


class AuthSettingsData(TypedDict):
    JWT_SECRET: str
    JWT_ALGORITHM: Literal[
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
    ]
    SESSION_TTL_MIN: int | float
    SESSION_REFRESH_THRESHOLD: int | float


class PostgresSettingsData(TypedDict):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DRIVER: str


def create_auth_settings_data(
    jwt_secret: str = "jwt_secret" + "0" * 32,
    jwt_algorithm: Literal[
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
    ] = "RS256",
    session_ttl_min: float = 2,
    session_refresh_threshold: float = 0.5,
) -> AuthSettingsData:
    return AuthSettingsData(
        JWT_SECRET=jwt_secret,
        JWT_ALGORITHM=jwt_algorithm,
        SESSION_TTL_MIN=session_ttl_min,
        SESSION_REFRESH_THRESHOLD=session_refresh_threshold,
    )


def create_postgres_settings_data(
    user: str = "user",
    password: str = "password",  # noqa: S107
    db: str = "db",
    host: str = "localhost",
    port: int = 5432,
    driver: str = "asyncpg",
) -> PostgresSettingsData:
    return PostgresSettingsData(
        POSTGRES_USER=user,
        POSTGRES_PASSWORD=password,
        POSTGRES_DB=db,
        POSTGRES_HOST=host,
        POSTGRES_PORT=port,
        POSTGRES_DRIVER=driver,
    )


class SQLAlchemySettingsData(TypedDict):
    DB_POOL_PRE_PING: bool
    DB_POOL_RECYCLE: int
    DB_POOL_SIZE: int
    DB_POOL_MAX_OVERFLOW: int
    DB_ECHO: bool
    DB_AUTO_FLUSH: bool
    DB_EXPIRE_ON_COMMIT: bool
    DB_FUTURE: bool


def create_sqlalchemy_settings_data(
    pool_pre_ping: bool | None = None,
    pool_recycle: int = 3600,
    pool_size: int = 10,
    max_overflow: int = 20,
    echo: bool | None = None,
    auto_flush: bool | None = None,
    expire_on_commit: bool | None = None,
    future: bool | None = None,
) -> SQLAlchemySettingsData:
    if pool_pre_ping is None:
        pool_pre_ping = True

    if echo is None:
        echo = False

    if auto_flush is None:
        auto_flush = False

    if expire_on_commit is None:
        expire_on_commit = False

    if future is None:
        future = True

    return SQLAlchemySettingsData(
        DB_POOL_PRE_PING=pool_pre_ping,
        DB_POOL_RECYCLE=pool_recycle,
        DB_POOL_SIZE=pool_size,
        DB_POOL_MAX_OVERFLOW=max_overflow,
        DB_ECHO=echo,
        DB_AUTO_FLUSH=auto_flush,
        DB_EXPIRE_ON_COMMIT=expire_on_commit,
        DB_FUTURE=future,
    )


class RedisSettingsData(TypedDict):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_CACHE_DB: int
    REDIS_WORKER_DB: int
    REDIS_SCHEDULE_SOURCE_DB: int
    REDIS_MAX_CONNECTIONS: int


def create_redis_settings_data(
    host: str = "localhost",
    port: int = 6379,
    user: str = "default",
    password: str = "password",  # noqa: S107
    cache_db: int = 0,
    worker_db: int = 1,
    schedule_source_db: int = 2,
    max_connections: int = 20,
) -> RedisSettingsData:
    return RedisSettingsData(
        REDIS_HOST=host,
        REDIS_PORT=port,
        REDIS_USER=user,
        REDIS_USER_PASSWORD=password,
        REDIS_CACHE_DB=cache_db,
        REDIS_WORKER_DB=worker_db,
        REDIS_SCHEDULE_SOURCE_DB=schedule_source_db,
        REDIS_MAX_CONNECTIONS=max_connections,
    )


class RabbitSettingsData(TypedDict):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str


def create_rabbit_settings_data(
    host: str = "localhost",
    port: int = 5672,
    user: str = "guest",
    password: str = "guest",  # noqa: S107
) -> RabbitSettingsData:
    return RabbitSettingsData(
        RABBITMQ_HOST=host,
        RABBITMQ_PORT=port,
        RABBITMQ_DEFAULT_USER=user,
        RABBITMQ_DEFAULT_PASS=password,
    )


class ASGISettingsData(TypedDict):
    UVICORN_HOST: str
    UVICORN_PORT: int
    FASTAPI_DEBUG: bool
    FASTAPI_ALLOW_CREDENTIALS: bool


def create_asgi_settings_data(
    host: str = "0.0.0.0",  # noqa: S104
    port: int = 8080,
    fastapi_debug: bool | None = None,
    allow_credentials: bool | None = None,
) -> ASGISettingsData:
    if allow_credentials is None:
        allow_credentials = False

    if fastapi_debug is None:
        fastapi_debug = True

    return ASGISettingsData(
        UVICORN_HOST=host,
        UVICORN_PORT=port,
        FASTAPI_DEBUG=fastapi_debug,
        FASTAPI_ALLOW_CREDENTIALS=allow_credentials,
    )


class S3SettingsData(TypedDict):
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_IMAGES_BUCKET: str


def create_s3_settings_data(
    host: str = "localhost",
    port: int = 9000,
    aws_access_key_id: str = "minioadmin",
    aws_secret_access_key: str = "minioadmin",  # noqa: S107
    images_bucket_name: str = "images",
) -> S3SettingsData:
    return S3SettingsData(
        MINIO_HOST=host,
        MINIO_PORT=port,
        MINIO_ROOT_USER=aws_access_key_id,
        MINIO_ROOT_PASSWORD=aws_secret_access_key,
        MINIO_IMAGES_BUCKET=images_bucket_name,
    )


class ObservabilitySettingsData(TypedDict):
    TEMPO_HOST: str
    TEMPO_GRPC_PORT: int


def create_observability_settings_data(
    tempo_host: str = "localhost",
    tempo_grpc_port: int = 4317,
) -> ObservabilitySettingsData:
    return ObservabilitySettingsData(
        TEMPO_HOST=tempo_host,
        TEMPO_GRPC_PORT=tempo_grpc_port,
    )


class HttpClientSettingsData(TypedDict):
    DEFAULT_HTTP_TIMEOUT: float
    DEFAULT_HTTP_VERIFY: bool | str
    DEFAULT_HTTP_FOLLOW_REDIRECTS: bool
    DEFAULT_HTTP_HTTP2: bool
    DEFAULT_HTTP_CLIENT_CERT: str | None
    DEFAULT_HTTP_CLIENT_KEY: str | None
    DEFAULT_HTTP_PROXIES: str | None
    DEFAULT_HTTP_MAX_CONNECTIONS: int
    DEFAULT_HTTP_MAX_KEEPALIVE: int
    DEFAULT_HTTP_KEEPALIVE_EXPIRY: float


def create_http_client_settings_data(
    default_timeout: float = 30.0,
    verify: bool | str | None = None,
    follow_redirects: bool | None = None,
    http2: bool | None = None,
    client_cert_path: str | None = None,
    client_key_path: str | None = None,
    proxy: str | None = None,
    max_connections: int = 100,
    max_keepalive_connections: int = 20,
    keepalive_expiry: float = 5.0,
) -> HttpClientSettingsData:
    if verify is None:
        verify = True

    if follow_redirects is None:
        follow_redirects = True

    if http2 is None:
        http2 = False

    return HttpClientSettingsData(
        DEFAULT_HTTP_TIMEOUT=default_timeout,
        DEFAULT_HTTP_VERIFY=verify,
        DEFAULT_HTTP_FOLLOW_REDIRECTS=follow_redirects,
        DEFAULT_HTTP_HTTP2=http2,
        DEFAULT_HTTP_CLIENT_CERT=client_cert_path,
        DEFAULT_HTTP_CLIENT_KEY=client_key_path,
        DEFAULT_HTTP_PROXIES=proxy,
        DEFAULT_HTTP_MAX_CONNECTIONS=max_connections,
        DEFAULT_HTTP_MAX_KEEPALIVE=max_keepalive_connections,
        DEFAULT_HTTP_KEEPALIVE_EXPIRY=keepalive_expiry,
    )


class TaskIQWorkerSettingsData(TypedDict):
    default_retry_count: int
    default_delay: int
    use_jitter: bool
    use_delay_exponent: bool
    max_delay_component: int
    durable_queue: bool
    durable_exchange: bool
    declare_exchange: bool
    PROMETHEUS_WORKER_SERVER_HOST: str
    PROMETHEUS_WORKER_SERVER_PORT: int


def create_taskiq_worker_settings_data(
    default_retry_count: int = 5,
    default_delay: int = 10,
    use_jitter: bool | None = None,
    use_delay_exponent: bool | None = None,
    max_delay_component: int = 120,
    durable_queue: bool | None = None,
    durable_exchange: bool | None = None,
    declare_exchange: bool | None = None,
    prometheus_server_address: str = "0.0.0.0",  # noqa: S104
    prometheus_server_port: int = 9090,
) -> TaskIQWorkerSettingsData:
    if use_jitter is None:
        use_jitter = True

    if use_delay_exponent is None:
        use_delay_exponent = True

    if durable_queue is None:
        durable_queue = True

    if durable_exchange is None:
        durable_exchange = True

    if declare_exchange is None:
        declare_exchange = True

    return TaskIQWorkerSettingsData(
        default_retry_count=default_retry_count,
        default_delay=default_delay,
        use_jitter=use_jitter,
        use_delay_exponent=use_delay_exponent,
        max_delay_component=max_delay_component,
        durable_queue=durable_queue,
        durable_exchange=durable_exchange,
        declare_exchange=declare_exchange,
        PROMETHEUS_WORKER_SERVER_HOST=prometheus_server_address,
        PROMETHEUS_WORKER_SERVER_PORT=prometheus_server_port,
    )
