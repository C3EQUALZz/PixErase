import pytest
from pydantic import ValidationError

from pix_erase.setup.config.cache import REDIS_DB_MAX, REDIS_DB_MIN, REDIS_MAX_CONNECTIONS_MIN, RedisConfig
from pix_erase.setup.config.database import PORT_MAX, PORT_MIN
from tests.unit.factories.settings_data import create_redis_settings_data


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(6379, id="common_redis_port"),
    ],
)
def test_redis_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_redis_settings_data(port=port)

    # Act & Assert
    RedisConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
    ],
)
def test_redis_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_redis_settings_data(port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        RedisConfig.model_validate(data)


@pytest.mark.parametrize(
    "db_index",
    [
        pytest.param(REDIS_DB_MIN, id="lower_bound"),
        pytest.param(REDIS_DB_MAX, id="upper_bound"),
        pytest.param(5, id="ordinary"),
    ],
)
def test_redis_db_accepts_correct_value(db_index: int) -> None:
    # Arrange
    data = create_redis_settings_data(
        cache_db=db_index,
        worker_db=db_index,
        schedule_source_db=db_index,
    )

    # Act & Assert
    RedisConfig.model_validate(data)


@pytest.mark.parametrize(
    "db_index",
    [
        pytest.param(REDIS_DB_MIN - 1, id="too_small"),
        pytest.param(REDIS_DB_MAX + 1, id="too_big"),
        pytest.param(-1, id="negative"),
        pytest.param(16, id="above_max"),
    ],
)
def test_redis_db_rejects_incorrect_value(db_index: int) -> None:
    # Arrange
    data = create_redis_settings_data(cache_db=db_index)

    # Act & Assert
    with pytest.raises(ValidationError):
        RedisConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_connections",
    [
        pytest.param(REDIS_MAX_CONNECTIONS_MIN, id="lower_bound"),
        pytest.param(20, id="ordinary"),
        pytest.param(100, id="large"),
    ],
)
def test_redis_max_connections_accepts_correct_value(max_connections: int) -> None:
    # Arrange
    data = create_redis_settings_data(max_connections=max_connections)

    # Act & Assert
    RedisConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_connections",
    [
        pytest.param(REDIS_MAX_CONNECTIONS_MIN - 1, id="too_small"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_redis_max_connections_rejects_incorrect_value(max_connections: int) -> None:
    # Arrange
    data = create_redis_settings_data(max_connections=max_connections)

    # Act & Assert
    with pytest.raises(ValidationError):
        RedisConfig.model_validate(data)

