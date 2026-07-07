"""add text column to generated audio

Revision ID: 5a36a85158f3
Revises: e2baa87abbf1
Create Date: 2026-07-06 06:37:22.318604
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a36a85158f3"
down_revision: Union[str, Sequence[str], None] = "e2baa87abbf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "generated_audio",
        sa.Column(
            "text",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
    )

    op.alter_column(
        "generated_audio",
        "text",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "generated_audio",
        "text",
    )