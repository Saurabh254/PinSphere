"""add description in images table

Revision ID: 81e7346f8f87
Revises: f2e1a69354d4
Create Date: 2025-02-06 19:46:28.545162

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "81e7346f8f87"
down_revision: Union[str, None] = "f2e1a69354d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("images", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("images", "description")
