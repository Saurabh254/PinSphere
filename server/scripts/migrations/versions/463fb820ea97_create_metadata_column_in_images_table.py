"""create metadata column in images table

Revision ID: 463fb820ea97
Revises: 81e7346f8f87
Create Date: 2025-02-10 16:00:02.035515

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "463fb820ea97"
down_revision: Union[str, None] = "81e7346f8f87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("images", sa.Column("_metadata", JSONB(), nullable=True))


def downgrade() -> None:
    op.drop_column("images", "_metadata")
