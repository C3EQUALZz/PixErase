from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.errors.user import RoleAssignmentNotPermittedError
from pix_erase.domain.user.events import (
    UserChangedEmailEvent,
    UserChangedNameEvent,
    UserChangedPasswordEvent,
    UserCreatedEvent,
)
from pix_erase.domain.user.ports.id_generator import UserIdGenerator
from pix_erase.domain.user.ports.password_hasher import PasswordHasher
from pix_erase.domain.user.values.raw_password import RawPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_name import Username
from pix_erase.domain.user.values.user_role import UserRole

if TYPE_CHECKING:
    from pix_erase.domain.user.values.hashed_password import HashedPassword
    from pix_erase.domain.user.values.user_id import UserID


class UserService(DomainService):
    """
    Domain service for users.
    """

    def __init__(
        self,
        password_hash_service: PasswordHasher,
        user_id_generator: UserIdGenerator,
    ) -> None:
        super().__init__()
        self._password_hasher: Final[PasswordHasher] = password_hash_service
        self._user_id_generator: Final[UserIdGenerator] = user_id_generator

    def create(
        self,
        email: UserEmail,
        name: Username,
        raw_password: RawPassword,
        role: UserRole = UserRole.USER,
    ) -> User:
        """
        Fabric method that creates a new user.

        :param email: Email of the user.
        :param name: Username of the user.
        :param raw_password: Raw password of the user.
        :param role: Role of the user.
        :return: User entity if all checks passed.

        NOTE:
            - produces event that user was created.
        """
        if role.is_assignable:
            msg: str = f"Assignment of role: {role} not permitted."
            raise RoleAssignmentNotPermittedError(msg)

        hashed_password: HashedPassword = self._password_hasher.hash(
            raw_password=raw_password,
        )

        new_user_id: UserID = self._user_id_generator()

        new_user: User = User(
            id=new_user_id,
            email=email,
            name=name,
            hashed_password=hashed_password,
            role=role,
        )

        new_event: UserCreatedEvent = UserCreatedEvent(
            user_id=new_user_id,
            email=str(new_user.email),
            name=str(new_user.name),
            role=new_user.role,
        )

        self._record_event(new_event)

        return new_user

    def is_password_valid(self, user: User, raw_password: RawPassword) -> bool:
        """
        Method that checks if the given password is valid for the given user.

        :param user: User entity which contains password.
        :param raw_password: Password to check.
        :return: True if the password is valid, False otherwise.
        """
        return self._password_hasher.verify(
            raw_password=raw_password,
            hashed_password=user.hashed_password,
        )

    def change_password(self, user: User, raw_password: RawPassword) -> None:
        """
        Method that changes the password of the given user.

        :param user: User entity which contains password.
        :param raw_password: New password to change.
        :return: None

        NOTE:
            - produces event that user changed the password.
        """

        hashed_password: HashedPassword = self._password_hasher.hash(raw_password)
        user.password_hash = hashed_password
        user.updated_at = datetime.now(UTC)

        new_event: UserChangedPasswordEvent = UserChangedPasswordEvent(
            user_id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=str(user.role),
        )

        self._record_event(new_event)

    def change_name(self, user: User, new_user_name: Username) -> None:
        """
        Method that changes the name of the given user.

        :param user: Existing user entity in a database.
        :param new_user_name: New username for entity.
        :return: Nothing.

        Note:
            - produces event that user changed the name.
        """
        old_user_name: Username = user.name
        user.name = new_user_name
        user.updated_at = datetime.now(UTC)

        new_event: UserChangedNameEvent = UserChangedNameEvent(
            user_id=user.id,
            old_name=str(old_user_name),
            new_name=str(new_user_name),
            role=str(user.role),
            email=str(user.email),
        )

        self._record_event(new_event)

    def change_email(self, user: User, new_email: UserEmail) -> None:
        """
        Method that changes the email of the given user.

        :param user: Existing user entity in a database.
        :param new_email: New email for entity.
        :return: Nothing.

        Note:
            - produces event that user changed the email.
        """
        old_email: UserEmail = user.email
        user.email = new_email
        user.updated_at = datetime.now(UTC)

        new_event: UserChangedEmailEvent = UserChangedEmailEvent(
            user_id=user.id,
            old_email=str(old_email),
            new_email=str(new_email),
            role=str(user.role),
            name=str(user.name),
        )

        self._record_event(new_event)