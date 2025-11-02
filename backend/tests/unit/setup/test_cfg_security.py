from datetime import timedelta

import pytest
from pydantic import ValidationError

from pix_erase.setup.config.security import AuthSettings
from tests.unit.factories.settings_data import create_auth_settings_data


@pytest.mark.parametrize(
    ("ttl", "expected"),
    [
        pytest.param(1, timedelta(minutes=1), id="boundary"),
        pytest.param(2.5, timedelta(minutes=2.5), id="ordinary"),
    ],
)
def test_auth_converts_ttl_to_timedelta(ttl: int | float, expected: timedelta) -> None:
    # Arrange
    data = create_auth_settings_data(session_ttl_min=ttl)

    # Act
    sut = AuthSettings.model_validate(data)

    # Assert
    assert sut.session_ttl_min == expected


@pytest.mark.parametrize(
    "ttl",
    [
        pytest.param("1", id="wrong_type"),
        pytest.param(0.99, id="too_small"),
    ],
)
def test_auth_rejects_invalid_ttl(ttl: int | str) -> None:
    # Arrange
    data = create_auth_settings_data(session_ttl_min=ttl)  # type: ignore[arg-type]

    # Act & Assert
    with pytest.raises((ValidationError, ValueError)):
        AuthSettings.model_validate(data)
