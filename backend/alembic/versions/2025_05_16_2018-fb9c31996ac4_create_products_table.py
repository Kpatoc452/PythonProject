"""create products table

Revision ID: fb9c31996ac4
Revises: 90580115952e
Create Date: 2025-05-16 20:18:36.729797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fb9c31996ac4"
down_revision: Union[str, None] = "90580115952e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Categories",
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Products",
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("sold", sa.Boolean(), nullable=False),
        sa.Column("seller_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["Categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["Users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Products")
    op.drop_table("Categories")
    # ### end Alembic commands ###
