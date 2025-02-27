"""add likes count in content table

Revision ID: 6961a0c1fd7a
Revises: c584eaf8575f
Create Date: 2025-02-26 11:57:07.820787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6961a0c1fd7a'
down_revision: Union[str, None] = 'c584eaf8575f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('contents', sa.Column('likes', sa.Integer(), nullable=True))
    op.execute('UPDATE contents SET likes = 0;')
    op.alter_column('contents', 'likes', nullable=False)



def downgrade() -> None:
    op.drop_column('contents', 'likes')
