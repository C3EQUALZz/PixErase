import pytest
from pydantic import ValidationError

from pix_erase.setup.config.database import PORT_MAX, PORT_MIN
from pix_erase.setup.config.rabbit import RabbitConfig
from tests.unit.factories.settings_data import create_rabbit_settings_data


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(5672, id="common_rabbitmq_port"),
    ],
)
def test_rabbit_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_rabbit_settings_data(port=port)

    # Act & Assert
    RabbitConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_rabbit_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_rabbit_settings_data(port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        RabbitConfig.model_validate(data)

