from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '709651871443'
down_revision: Union[str, None] = 'c0baea2b3c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_pkey")
    op.execute("ALTER TABLE users ADD PRIMARY KEY (id)")

    op.create_table('comments',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('content_id', sa.UUID(), sa.ForeignKey('contents.id', ondelete='CASCADE'), nullable=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('parent_id', sa.UUID(), sa.ForeignKey('comments.id', ondelete='CASCADE'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)

    op.create_table('contentlikes',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content_id', sa.UUID(), sa.ForeignKey('contents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('liked', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('user_id', 'content_id')
    )

    op.create_index(op.f('ix_contentlikes_id'), 'contentlikes', ['id'], unique=False)

    op.create_table('comment_likes',
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('comment_id', sa.UUID(), sa.ForeignKey('comments.id', ondelete='CASCADE'), primary_key=True),
    )

    # Ensure users table has a proper foreign key for contents
    op.create_foreign_key("user_id_fk", 'contents', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("user_id_fk", 'contents', type_='foreignkey')
    op.drop_table('comment_likes')
    op.drop_index(op.f('ix_contentlikes_id'), table_name='contentlikes')
    op.drop_table('contentlikes')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###
