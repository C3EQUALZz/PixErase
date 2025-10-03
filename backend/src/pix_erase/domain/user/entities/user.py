from dataclasses import dataclass, field

from pix_erase.domain.common.entities.base_aggregate import BaseAggregateRoot
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.user.values.hashed_password import HashedPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.domain.user.values.user_name import Username
from pix_erase.domain.user.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseAggregateRoot[UserID]):
    """
    Aggregate which represents a user account in system.
    This entity has fields that are listed here in the documentation link:
    - https://wiki.yandex.ru/homepage/assistent-jelja/dokumentacija-k-sprintu-7/texnicheskoe-opisanie-zadach/3-sozdanie-modeli-dannyx-i-api-dlja-soobshhenii/3.9-model-polzovatelja-i-rolec/

    NOTE:
        - id is UUID type for unique
        - email must be valid type. Please check for real email before creating an account.
        - password must be hashed before creating an account. Check for hash in service.
        - role. For description check enum UserRole.
        - is_active. True if user not blocked by admin. False otherwise.
    """

    email: UserEmail
    name: Username
    hashed_password: HashedPassword
    role: UserRole = field(default_factory=lambda: UserRole.USER)
    is_active: bool = field(default_factory=lambda: True)
    images: list[ImageID] = field(default_factory=lambda: [])
