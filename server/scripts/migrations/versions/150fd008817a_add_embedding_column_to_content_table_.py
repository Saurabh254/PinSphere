"""add embedding column to content table for vector search

Revision ID: 150fd008817a
Revises: 45ec72a5ba3a
Create Date: 2025-03-26 20:07:46.532637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy
# revision identifiers, used by Alembic.
revision: str = '150fd008817a'
down_revision: Union[str, None] = '45ec72a5ba3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('contents', sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(), nullable=True, index=True))


def downgrade() -> None:
    op.drop_column('contents', 'embedding')
