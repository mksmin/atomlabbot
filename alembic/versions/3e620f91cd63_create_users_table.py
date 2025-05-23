"""create users table

Revision ID: 3e620f91cd63
Revises: 
Create Date: 2024-10-25 00:15:57.699260

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e620f91cd63"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("tg_username", sa.String(length=30), nullable=True),
        sa.Column(
            "karma_start_value",
            sa.Integer(),
            server_default="20",
            nullable=False,
        ),
        sa.Column(
            "total_karma", sa.Integer(), server_default="0", nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tg_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
