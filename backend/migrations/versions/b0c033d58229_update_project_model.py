"""update project model

Revision ID: b0c033d58229
Revises: 46d91755ca76
Create Date: 2026-07-03 14:52:14.288643

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b0c033d58229"
down_revision: Union[str, Sequence[str], None] = "46d91755ca76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "projects",
        sa.Column(
            "status",
            sa.String(length=50),
            server_default="script_generated",
            nullable=False,
        ),
    )

    op.alter_column(
        "projects",
        "hashtags",
        existing_type=sa.TEXT(),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        existing_nullable=False,
        postgresql_using="hashtags::jsonb",
    )

    op.alter_column(
        "projects",
        "image_prompts",
        existing_type=sa.TEXT(),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        existing_nullable=False,
        postgresql_using="image_prompts::jsonb",
    )

    op.alter_column(
        "projects",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )

    op.alter_column(
        "projects",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "projects",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )

    op.alter_column(
        "projects",
        "image_prompts",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.TEXT(),
        existing_nullable=False,
        postgresql_using="image_prompts::text",
    )

    op.alter_column(
        "projects",
        "hashtags",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.TEXT(),
        existing_nullable=False,
        postgresql_using="hashtags::text",
    )

    op.drop_column("projects", "status")