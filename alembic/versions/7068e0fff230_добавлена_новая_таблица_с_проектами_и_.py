"""Добавлена новая таблица с проектами и добавлен TimestampMixin

Revision ID: 7068e0fff230
Revises: 94f98ddcbfdc
Create Date: 2025-03-07 19:40:08.834095

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7068e0fff230"
down_revision: Union[str, None] = "94f98ddcbfdc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("prj_name", sa.String(length=50), nullable=True),
        sa.Column("prj_description", sa.String(length=200), nullable=True),
        sa.Column("prj_owner", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["prj_owner"],
            ["users.tg_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "chatandusers", sa.Column("created_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "users", sa.Column("user_status", sa.String(length=30), nullable=True)
    )
    op.add_column(
        "users", sa.Column("created_at", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "created_at")
    op.drop_column("users", "user_status")
    op.drop_column("chatandusers", "created_at")
    op.drop_table("projects")
    # ### end Alembic commands ###
