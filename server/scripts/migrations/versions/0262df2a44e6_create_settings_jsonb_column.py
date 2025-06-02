"""create settings jsonb column

Revision ID: 0262df2a44e6
Revises: 150fd008817a
Create Date: 2025-06-02 15:22:05.841570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '0262df2a44e6'
down_revision: Union[str, None] = '150fd008817a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('settings', JSONB, nullable=True, server_default='{}'))


def downgrade() -> None:
    op.drop_column('users', 'settings')
