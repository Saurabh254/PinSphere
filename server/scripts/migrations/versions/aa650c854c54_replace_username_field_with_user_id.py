"""replace username field with user_id

Revision ID: aa650c854c54
Revises: b528836febac
Create Date: 2025-03-08 14:30:21.087233

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa650c854c54"
down_revision: Union[str, None] = "b528836febac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("contents", sa.Column("user_id", sa.UUID(), nullable=False))
    op.drop_column("contents", "username")


def downgrade() -> None:
    op.add_column(
        "contents", sa.Column("username", sa.VARCHAR(length=50), nullable=False)
    )
    op.drop_column("contents", "user_id")
