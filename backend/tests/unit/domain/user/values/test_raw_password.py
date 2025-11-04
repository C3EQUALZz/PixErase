import pytest

from pix_erase.domain.user.errors.raw_password import WeakPasswordWasProvidedError
from pix_erase.domain.user.values.raw_password import MIN_PASSWORD_LENGTH, RawPassword


def test_accepts_boundary_length() -> None:
    password = "a" * MIN_PASSWORD_LENGTH

    RawPassword(password)


def test_rejects_out_of_bounds_length() -> None:
    password = "a" * (MIN_PASSWORD_LENGTH - 1)

    with pytest.raises(WeakPasswordWasProvidedError):
        RawPassword(password)
