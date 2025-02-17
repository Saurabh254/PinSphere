"""renamed images table to contents table

Revision ID: 47946b048d2a
Revises: 463fb820ea97
Create Date: 2025-02-16 19:44:53.858638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '47946b048d2a'
down_revision: Union[str, None] = '463fb820ea97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contents',
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('blurhash', sa.String(length=50), nullable=True),
    sa.Column('content_key', sa.String(length=256), nullable=False),
    sa.Column('status', sa.Enum('PROCESSING', 'PROCESSED', name='content_processing_enum'), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contents_id'), 'contents', ['id'], unique=False)
    op.drop_index('ix_images_created_at', table_name='images')
    op.drop_index('ix_images_updated_at', table_name='images')
    op.drop_table('images')
    op.execute('DROP TYPE image_processing_enum;')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('blurhash', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('image_key', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('PROCESSING', 'PROCESSED', name='image_processing_enum'), autoincrement=False, nullable=False),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('_metadata', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], name='images_username_fkey'),
    sa.PrimaryKeyConstraint('id', name='images_pkey'),
    sa.UniqueConstraint('image_key', name='images_image_key_key')
    )
    op.create_index('ix_images_updated_at', 'images', ['updated_at'], unique=False)
    op.create_index('ix_images_created_at', 'images', ['created_at'], unique=False)
    op.drop_index(op.f('ix_contents_id'), table_name='contents')
    op.drop_table('contents')
    op.execute("DROP TYPE content_processing_enum;")
    # ### end Alembic commands ###
