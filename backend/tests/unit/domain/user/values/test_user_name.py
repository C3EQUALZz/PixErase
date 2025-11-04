import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.user.errors.user import (
    BadUserNameError,
    TooBigUserAccountNameError,
    TooSmallUserAccountNameError,
    UserAccountNameCantBeEmptyError,
)
from pix_erase.domain.user.values.user_name import MAX_LENGTH_OF_USERNAME, MIN_LENGTH_OF_USERNAME, Username


@pytest.mark.parametrize(
    "username",
    [
        pytest.param("a" * MIN_LENGTH_OF_USERNAME, id="min_len"),
        pytest.param("a" * MAX_LENGTH_OF_USERNAME, id="max_len"),
    ],
)
def test_accepts_boundary_length(username: str) -> None:
    Username(username)


@pytest.mark.parametrize(
    ("username", "expected_error"),
    [
        pytest.param("a" * (MIN_LENGTH_OF_USERNAME - 1), TooSmallUserAccountNameError, id="too_small_len"),
        pytest.param("a" * (MAX_LENGTH_OF_USERNAME + 1), TooBigUserAccountNameError, id="too_big_len"),
        pytest.param("", UserAccountNameCantBeEmptyError, id="empty"),
    ],
)
def test_rejects_out_of_bounds_length(username: str, expected_error: type[DomainFieldError]) -> None:
    with pytest.raises(expected_error):
        Username(username)


@pytest.mark.parametrize(
    "username",
    [
        "username",
        "user.name",
        "user-name",
        "user_name",
        "user123",
        "user.name123",
        "u.ser-name123",
        "u-ser_name",
        "u-ser.name",
    ],
)
def test_accepts_correct_names(username: str) -> None:
    Username(username)


@pytest.mark.parametrize(
    "username",
    [
        ".username",
        "-username",
        "_username",
        "username.",
        "username-",
        "username_",
        "user..name",
        "user--name",
        "user__name",
        "user!name",
        "user@name",
        "user#name",
    ],
)
def test_rejects_incorrect_names(username: str) -> None:
    with pytest.raises(BadUserNameError):
        Username(username)
