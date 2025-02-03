"""create images table

Revision ID: f2e1a69354d4
Revises: 53c200918d00
Create Date: 2025-02-03 19:41:28.512968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f2e1a69354d4'
down_revision: Union[str, None] = '53c200918d00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('images',
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('blurhash', sa.String(length=50), nullable=True),
    sa.Column('image_key', sa.String(length=256), nullable=False, unique=True),
    sa.Column('status', sa.Enum('PROCESSING', 'PROCESSED', name='image_processing_enum'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), primary_key=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, index=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, index=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_photos')
    op.execute("DROP TYPE status_enum")

def downgrade() -> None:
    op.create_table('user_photos',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('image_key', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('PROCESSED', 'PROCESSING', name='status_enum'), autoincrement=False, nullable=False),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('blurhash', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], name='user_photos_username_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_photos_pkey')
    )
    op.drop_table('images')
    op.execute("DROP TYPE image_processing_enum")
