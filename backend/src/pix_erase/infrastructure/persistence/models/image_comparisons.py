import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from pix_erase.domain.image.entities.image_comparison import ImageComparison
from pix_erase.infrastructure.persistence.models.base import mapper_registry

image_comparisons_table: sa.Table = sa.Table(
    "image_comparisons",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
    sa.Column("first_image_id", sa.UUID(as_uuid=True), nullable=False, index=True),
    sa.Column("second_image_id", sa.UUID(as_uuid=True), nullable=False, index=True),
    sa.Column("scores", JSONB, nullable=False),
    sa.Column("different_names", sa.Boolean, nullable=False),
    sa.Column("different_width", sa.Boolean, nullable=False),
    sa.Column("different_height", sa.Boolean, nullable=False),
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
    sa.Index(
        "ix_image_comparisons_image_ids",
        "first_image_id",
        "second_image_id",
        unique=False,
    ),
)


def map_image_comparisons_table() -> None:
    mapper_registry.map_imperatively(
        ImageComparison,
        image_comparisons_table,
        properties={
            "id": image_comparisons_table.c.id,
            "first_image_id": image_comparisons_table.c.first_image_id,
            "second_image_id": image_comparisons_table.c.second_image_id,
            "scores": image_comparisons_table.c.scores,
            "different_names": image_comparisons_table.c.different_names,
            "different_width": image_comparisons_table.c.different_width,
            "different_height": image_comparisons_table.c.different_height,
            "created_at": image_comparisons_table.c.created_at,
            "updated_at": image_comparisons_table.c.updated_at,
        },
        column_prefix="_",
    )
