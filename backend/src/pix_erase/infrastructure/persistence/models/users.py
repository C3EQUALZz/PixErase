import sqlalchemy as sa
from sqlalchemy.orm import composite

from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.hashed_password import HashedPassword
from pix_erase.domain.user.values.user_email import UserEmail
from pix_erase.domain.user.values.user_name import Username
from pix_erase.domain.user.values.user_role import UserRole
from pix_erase.infrastructure.persistence.models.base import mapper_registry

users_table: sa.Table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("email", sa.String(50), nullable=False, unique=True),
    sa.Column("name", sa.String(20), nullable=False),
    sa.Column("hashed_password", sa.LargeBinary(), nullable=False),
    sa.Column("role", sa.Enum(UserRole), nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=True,
    ),
)


def map_users_table() -> None:
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "id": users_table.c.id,
            "email": composite(UserEmail, users_table.c.email),
            "name": composite(Username, users_table.c.name),
            "hashed_password": composite(HashedPassword, users_table.c.hashed_password),
            "role": users_table.c.role,
            "is_active": users_table.c.is_active,
            "created_at": users_table.c.created_at,
            "updated_at": users_table.c.updated_at,
        },
        column_prefix="_"
    )
