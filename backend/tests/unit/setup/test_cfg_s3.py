import pytest
from pydantic import ValidationError

from pix_erase.setup.config.database import PORT_MAX, PORT_MIN
from pix_erase.setup.config.s3 import S3Config
from tests.unit.factories.settings_data import create_s3_settings_data


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN, id="lower_bound"),
        pytest.param(PORT_MAX, id="upper_bound"),
        pytest.param(9000, id="common_minio_port"),
    ],
)
def test_s3_port_accepts_correct_value(port: int) -> None:
    # Arrange
    data = create_s3_settings_data(port=port)

    # Act & Assert
    S3Config.model_validate(data)


@pytest.mark.parametrize(
    "port",
    [
        pytest.param(PORT_MIN - 1, id="too_small"),
        pytest.param(PORT_MAX + 1, id="too_big"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_s3_port_rejects_incorrect_value(port: int) -> None:
    # Arrange
    data = create_s3_settings_data(port=port)

    # Act & Assert
    with pytest.raises(ValidationError):
        S3Config.model_validate(data)
