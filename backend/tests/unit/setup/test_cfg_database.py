import pytest
from pydantic import PostgresDsn, ValidationError

from pix_erase.setup.config.database import (
    POOL_OVERFLOW_MIN,
    POOL_RECYCLE_MIN,
    POOL_SIZE_MAX,
    POOL_SIZE_MIN,
    PORT_MAX,
    PORT_MIN,
    PostgresConfig,
    SQLAlchemyConfig,
)
from tests.unit.factories.settings_data import (
    create_postgres_settings_data,
    create_sqlalchemy_settings_data,
)


def test_postgres_host_overridden_by_env_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    env_host = "changed"
    monkeypatch.setenv("POSTGRES_HOST", env_host)
    data = create_postgres_settings_data(host="initial")

    # Act
    sut = PostgresConfig.model_validate(data)

    # Assert
    assert sut.host == env_host


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(5432, id="common_postgres_port"),
    ],
)
def test_postgres_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_postgres_settings_data(port=port)

    # Act & Assert
    PostgresConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_postgres_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_postgres_settings_data(port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        PostgresConfig.model_validate(data)


def test_postgres_dsn_builds_valid_uri_from_fields() -> None:
    # Arrange
    data = create_postgres_settings_data(
        user="alice",
        password="secret",
        db="my_db",
        host="localhost",
        port=5678,
        driver="psycopg2",
    )

    # Act
    sut = PostgresConfig.model_validate(data)

    # Assert
    assert sut.uri == "postgresql+psycopg2://alice:secret@localhost:5678/my_db"
    assert PostgresDsn(sut.uri)


@pytest.mark.parametrize(
    "pool_size",
    [
        pytest.param(POOL_SIZE_MIN, id="lower_bound"),
        pytest.param(POOL_SIZE_MAX, id="upper_bound"),
        pytest.param(10, id="ordinary"),
    ],
)
def test_sqlalchemy_pool_size_accepts_correct_value(pool_size: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(pool_size=pool_size)

    # Act & Assert
    SQLAlchemyConfig.model_validate(data)


@pytest.mark.parametrize(
    "pool_size",
    [
        pytest.param(POOL_SIZE_MIN - 1, id="too_small"),
        pytest.param(POOL_SIZE_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
    ],
)
def test_sqlalchemy_pool_size_rejects_incorrect_value(pool_size: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(pool_size=pool_size)

    # Act & Assert
    with pytest.raises(ValidationError):
        SQLAlchemyConfig.model_validate(data)


@pytest.mark.parametrize(
    "pool_recycle",
    [
        pytest.param(POOL_RECYCLE_MIN, id="lower_bound"),
        pytest.param(3600, id="common_value"),
        pytest.param(7200, id="large_value"),
    ],
)
def test_sqlalchemy_pool_recycle_accepts_correct_value(pool_recycle: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(pool_recycle=pool_recycle)

    # Act & Assert
    SQLAlchemyConfig.model_validate(data)


@pytest.mark.parametrize(
    "pool_recycle",
    [
        pytest.param(POOL_RECYCLE_MIN - 1, id="too_small"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_sqlalchemy_pool_recycle_rejects_incorrect_value(pool_recycle: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(pool_recycle=pool_recycle)

    # Act & Assert
    with pytest.raises(ValidationError):
        SQLAlchemyConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_overflow",
    [
        pytest.param(POOL_OVERFLOW_MIN, id="lower_bound"),
        pytest.param(20, id="ordinary"),
        pytest.param(100, id="large"),
    ],
)
def test_sqlalchemy_max_overflow_accepts_correct_value(max_overflow: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(max_overflow=max_overflow)

    # Act & Assert
    SQLAlchemyConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_overflow",
    [
        pytest.param(POOL_OVERFLOW_MIN - 1, id="too_small"),
        pytest.param(-1, id="negative"),
    ],
)
def test_sqlalchemy_max_overflow_rejects_incorrect_value(max_overflow: int) -> None:
    # Arrange
    data = create_sqlalchemy_settings_data(max_overflow=max_overflow)

    # Act & Assert
    with pytest.raises(ValidationError):
        SQLAlchemyConfig.model_validate(data)
