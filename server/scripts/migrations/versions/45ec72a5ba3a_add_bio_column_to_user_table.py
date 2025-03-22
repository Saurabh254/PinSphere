"""add bio column to user table

Revision ID: 45ec72a5ba3a
Revises: 709651871443
Create Date: 2025-03-21 16:16:01.373267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '45ec72a5ba3a'
down_revision: Union[str, None] = '709651871443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('users', sa.Column('bio', sa.String(length=100), nullable=True))



def downgrade() -> None:
    op.drop_column('users', 'bio')
