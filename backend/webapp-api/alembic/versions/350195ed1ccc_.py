"""empty message

Revision ID: 350195ed1ccc
Revises: d615596d0a5c
Create Date: 2026-02-06 11:54:13.804313

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "350195ed1ccc"
down_revision: str | None = "d615596d0a5c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    conn = op.get_bind()

    result = conn.execute(
        text("""
            SELECT constraint_name 
            FROM information_schema.table_constraints 
            WHERE table_name = 'brands' 
            AND constraint_type = 'FOREIGN KEY'
            AND constraint_name LIKE '%archetype%'
        """)
    )
    constraint_name = result.scalar()

    if constraint_name:
        op.drop_constraint(constraint_name, "brands", type_="foreignkey")

    result = conn.execute(
        text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'brands' 
            AND column_name = 'archetype'
        """)
    )
    if result.scalar():
        op.drop_column("brands", "archetype")


def downgrade() -> None:
    op.add_column("brands", sa.Column("archetype", sa.VARCHAR(), nullable=True))
    op.create_foreign_key(
        "brands_archetype_fkey",
        "brands",
        "brand_archetypes",
        ["archetype"],
        ["name"],
    )
