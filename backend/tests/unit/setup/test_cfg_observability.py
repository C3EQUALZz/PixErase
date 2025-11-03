import pytest
from pydantic import ValidationError

from pix_erase.setup.config.database import PORT_MAX, PORT_MIN
from pix_erase.setup.config.obversability import ObservabilityConfig
from tests.unit.factories.settings_data import create_observability_settings_data


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(4317, id="common_tempo_grpc_port"),
    ],
)
def test_observability_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_observability_settings_data(tempo_grpc_port=port)

    # Act & Assert
    ObservabilityConfig.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_observability_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_observability_settings_data(tempo_grpc_port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        ObservabilityConfig.model_validate(data)


