from uuid import uuid4

from typing_extensions import override

from pix_erase.domain.user.ports.id_generator import UserIdGenerator
from pix_erase.domain.user.values.user_id import UserID


class UUID4UserIdGenerator(UserIdGenerator):
    @override
    def __call__(self) -> UserID:
        return UserID(uuid4())
