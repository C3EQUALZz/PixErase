from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_role import UserRole
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.hashed_password import HashedPassword
from pix_erase.domain.user.values.user_name import Username

from tests.unit.factories.value_objects import (
    create_password_hash,
    create_user_email,
    create_user_id,
    create_username,
)


def create_user(
        user_id: UserID | None = None,
        username: Username | None = None,
        password_hash: HashedPassword | None = None,
        role: UserRole = UserRole.USER,
        email: UserEmail | None = None,
        is_active: bool = True,
) -> User:
    return User(
        id=user_id or create_user_id(),
        email=email or create_user_email(),
        name=username or create_username(),
        hashed_password=password_hash or create_password_hash(),
        role=role,
        is_active=is_active,
    )
