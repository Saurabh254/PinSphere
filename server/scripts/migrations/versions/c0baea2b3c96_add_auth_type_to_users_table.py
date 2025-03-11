"""add_auth_type_to_users_table

Revision ID: c0baea2b3c96
Revises: aa650c854c54
Create Date: 2025-03-10 20:43:01.757662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c0baea2b3c96'
down_revision: Union[str, None] = 'aa650c854c54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define Enum type outside to avoid issues during downgrade
auth_type_enum = sa.Enum('local', 'google', name='authtype')

def upgrade() -> None:
    # Create enum type in DB first
    auth_type_enum.create(op.get_bind(), checkfirst=True)

    # Add column using the enum type
    op.add_column('users', sa.Column('auth_type', auth_type_enum, nullable=False, server_default='local'))

    # Modify password and password_salt columns to be nullable
    op.alter_column('users', 'password',
                    existing_type=postgresql.BYTEA(),
                    nullable=True)
    op.alter_column('users', 'password_salt',
                    existing_type=postgresql.BYTEA(),
                    nullable=True)

def downgrade() -> None:
    # Revert password and password_salt to NOT NULL
    op.alter_column('users', 'password_salt',
                    existing_type=postgresql.BYTEA(),
                    nullable=False)
    op.alter_column('users', 'password',
                    existing_type=postgresql.BYTEA(),
                    nullable=False)

    # Drop the auth_type column
    op.drop_column('users', 'auth_type')

    # Drop the enum type
    auth_type_enum.drop(op.get_bind(), checkfirst=True)
