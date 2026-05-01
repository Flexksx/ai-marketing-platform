"""add content generation jobs

Revision ID: ac604a79a9d9
Revises: 350195ed1ccc
Create Date: 2026-02-06 11:55:15.007367

"""
from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = 'ac604a79a9d9'
down_revision: str | None = '350195ed1ccc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

