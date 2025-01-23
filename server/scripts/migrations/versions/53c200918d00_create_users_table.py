"""create users table

Revision ID: 53c200918d00
Revises:
Create Date: 2025-01-18 11:35:41.249093

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "53c200918d00"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=50), nullable=False),
        sa.Column("password_salt", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_table(
        "user_photos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("image_key", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PROCESSED", "PROCESSING", name="status_enum"),
            nullable=False,
        ),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("blurhash", sa.String(length=50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["username"],
            ["users.username"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("user_photos")
    op.execute("DROP TYPE status_enum;")
    op.drop_table("users")
