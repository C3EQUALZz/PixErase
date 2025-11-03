import pytest
from pydantic import ValidationError

from pix_erase.setup.config.http import (
    HTTP_CONNECTIONS_MIN,
    HTTP_KEEPALIVE_EXPIRY_MIN,
    HTTP_TIMEOUT_MIN,
    HttpClientConfig,
)
from tests.unit.factories.settings_data import create_http_client_settings_data


@pytest.mark.parametrize(
    "timeout",
    [
        pytest.param(HTTP_TIMEOUT_MIN, id="lower_bound"),
        pytest.param(30.0, id="default"),
        pytest.param(60.0, id="large"),
    ],
)
def test_http_timeout_accepts_correct_value(timeout: float) -> None:
    # Arrange
    data = create_http_client_settings_data(default_timeout=timeout)

    # Act & Assert
    HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "timeout",
    [
        pytest.param(HTTP_TIMEOUT_MIN - 0.1, id="too_small"),
        pytest.param(0.0, id="zero"),
        pytest.param(-1.0, id="negative"),
    ],
)
def test_http_timeout_rejects_incorrect_value(timeout: float) -> None:
    # Arrange
    data = create_http_client_settings_data(default_timeout=timeout)

    # Act & Assert
    with pytest.raises(ValidationError):
        HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_connections",
    [
        pytest.param(HTTP_CONNECTIONS_MIN, id="lower_bound"),
        pytest.param(100, id="default"),
        pytest.param(500, id="large"),
    ],
)
def test_http_max_connections_accepts_correct_value(max_connections: int) -> None:
    # Arrange
    data = create_http_client_settings_data(max_connections=max_connections)

    # Act & Assert
    HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "max_connections",
    [
        pytest.param(HTTP_CONNECTIONS_MIN - 1, id="too_small"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_http_max_connections_rejects_incorrect_value(max_connections: int) -> None:
    # Arrange
    data = create_http_client_settings_data(max_connections=max_connections)

    # Act & Assert
    with pytest.raises(ValidationError):
        HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "keepalive_connections",
    [
        pytest.param(HTTP_CONNECTIONS_MIN, id="lower_bound"),
        pytest.param(20, id="default"),
        pytest.param(50, id="large"),
    ],
)
def test_http_max_keepalive_connections_accepts_correct_value(keepalive_connections: int) -> None:
    # Arrange
    data = create_http_client_settings_data(max_keepalive_connections=keepalive_connections)

    # Act & Assert
    HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "keepalive_connections",
    [
        pytest.param(HTTP_CONNECTIONS_MIN - 1, id="too_small"),
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_http_max_keepalive_connections_rejects_incorrect_value(keepalive_connections: int) -> None:
    # Arrange
    data = create_http_client_settings_data(max_keepalive_connections=keepalive_connections)

    # Act & Assert
    with pytest.raises(ValidationError):
        HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "keepalive_expiry",
    [
        pytest.param(HTTP_KEEPALIVE_EXPIRY_MIN, id="lower_bound"),
        pytest.param(5.0, id="default"),
        pytest.param(30.0, id="large"),
    ],
)
def test_http_keepalive_expiry_accepts_correct_value(keepalive_expiry: float) -> None:
    # Arrange
    data = create_http_client_settings_data(keepalive_expiry=keepalive_expiry)

    # Act & Assert
    HttpClientConfig.model_validate(data)


@pytest.mark.parametrize(
    "keepalive_expiry",
    [
        pytest.param(HTTP_KEEPALIVE_EXPIRY_MIN - 0.1, id="too_small"),
        pytest.param(0.0, id="zero"),
        pytest.param(-1.0, id="negative"),
    ],
)
def test_http_keepalive_expiry_rejects_incorrect_value(keepalive_expiry: float) -> None:
    # Arrange
    data = create_http_client_settings_data(keepalive_expiry=keepalive_expiry)

    # Act & Assert
    with pytest.raises(ValidationError):
        HttpClientConfig.model_validate(data)


