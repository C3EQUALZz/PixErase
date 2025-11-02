from typing import cast
from unittest.mock import create_autospec

import pytest

from pix_erase.domain.user.ports.id_generator import UserIdGenerator
from pix_erase.domain.user.ports.password_hasher import PasswordHasher


@pytest.fixture
def user_id_generator() -> UserIdGenerator:
    return cast(UserIdGenerator, create_autospec(UserIdGenerator))


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return cast(PasswordHasher, create_autospec(PasswordHasher))
