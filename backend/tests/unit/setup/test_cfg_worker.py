import pytest
from pydantic import ValidationError

from pix_erase.setup.config.database import PORT_MAX, PORT_MIN
from pix_erase.setup.config.worker import (
    DELAY_MIN,
    MAX_DELAY_COMPONENT_MIN,
    RETRY_COUNT_MIN,
    TaskIQWorkerConfig,
)
from tests.unit.factories.settings_data import create_taskiq_worker_settings_data


@pytest.mark.parametrize(
    "retry_count",
    [
        pytest.param(RETRY_COUNT_MIN, id="lower_bound"),
        pytest.param(5, id="default"),
        pytest.param(10, id="large"),
    ],
)
def test_taskiq_retry_count_accepts_correct_value(retry_count: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(default_retry_count=retry_count)

    # Act & Assert
    TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "retry_count",
    [
        pytest.param(RETRY_COUNT_MIN - 1, id="too_small"),
        pytest.param(-1, id="negative"),
    ],
)
def test_taskiq_retry_count_rejects_incorrect_value(retry_count: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(default_retry_count=retry_count)

    # Act & Assert
    with pytest.raises(ValidationError):
        TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "delay",
    [
        pytest.param(DELAY_MIN, id="lower_bound"),
        pytest.param(10, id="default"),
        pytest.param(60, id="large"),
    ],
)
def test_taskiq_delay_accepts_correct_value(delay: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(default_delay=delay)

    # Act & Assert
    TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "delay",
    [
        pytest.param(DELAY_MIN - 1, id="too_small"),
        pytest.param(-1, id="negative"),
    ],
)
def test_taskiq_delay_rejects_incorrect_value(delay: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(default_delay=delay)

    # Act & Assert
    with pytest.raises(ValidationError):
        TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_delay_component",
    [
        pytest.param(MAX_DELAY_COMPONENT_MIN, id="lower_bound"),
        pytest.param(120, id="default"),
        pytest.param(300, id="large"),
    ],
)
def test_taskiq_max_delay_component_accepts_correct_value(max_delay_component: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(max_delay_component=max_delay_component)

    # Act & Assert
    TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_delay_component",
    [
        pytest.param(MAX_DELAY_COMPONENT_MIN - 1, id="too_small"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_taskiq_max_delay_component_rejects_incorrect_value(max_delay_component: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(max_delay_component=max_delay_component)

    # Act & Assert
    with pytest.raises(ValidationError):
        TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(9090, id="default_prometheus_port"),
    ],
)
def test_taskiq_prometheus_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(prometheus_server_port=port)

    # Act & Assert
    TaskIQWorkerConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_taskiq_prometheus_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_taskiq_worker_settings_data(prometheus_server_port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        TaskIQWorkerConfig.model_validate(data)
