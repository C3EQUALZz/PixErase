"""Init admin in system

Revision ID: 2fb25e662e00
Revises: 55d2439e8bf0
Create Date: 2025-10-04 21:46:16.097742

"""
from collections.abc import Sequence
import uuid
from sqlalchemy import text
from alembic import op
import sqlalchemy as sa

from pix_erase.domain.user.values.user_role import UserRole

# revision identifiers, used by Alembic.
revision: str = "2fb25e662e00"
down_revision: str | Sequence[str] | None = "55d2439e8bf0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    admin_id = uuid.uuid4()
    op.execute(
        sa.text("""
                INSERT INTO users (id, email, name, hashed_password, role, is_active, image_ids, created_at, updated_at)
                VALUES (:id, :email, :name, :hashed_password, :role, :is_active, :image_ids, NOW(), NOW())
                """).bindparams(
            sa.bindparam('id', admin_id, type_=sa.UUID),
            sa.bindparam('email', 'admin@pixerase.com', type_=sa.String),
            sa.bindparam('name', 'admin', type_=sa.String),
            sa.bindparam('hashed_password', b'$2b$12$4fu0v.ZGLAbPR47DZPokseGqAEuH8Pj8xZs6sZHIWeXvkzE/qP38y',
                         type_=sa.LargeBinary),
            sa.bindparam('role', 'SUPER_ADMIN', type_=sa.Enum(name='userrole')),
            sa.bindparam('is_active', True, type_=sa.Boolean),
            sa.bindparam('image_ids', [], type_=sa.ARRAY(sa.UUID))
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем администратора
    delete_admin = text("DELETE FROM users WHERE email = 'admin@pixerase.com'")

    from alembic import op
    op.execute(delete_admin)