"""Fix campaigns channels column type for ContentChannelName enum

Revision ID: 4ac2c8cd6657
Revises: ee2c545616c7
Create Date: 2025-12-20 21:20:07.147866

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4ac2c8cd6657'
down_revision: str | None = 'ee2c545616c7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE TYPE contentchannelname AS ENUM ('INSTAGRAM', 'LINKEDIN')")

    op.alter_column('campaigns', 'channels',
               existing_type=postgresql.ARRAY(postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel')),
               type_=sa.ARRAY(sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname')),
               existing_nullable=True,
               postgresql_using="channels::text[]::contentchannelname[]")
    op.alter_column('post_generation_jobs', 'channel',
               existing_type=postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel'),
               type_=sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname'),
               existing_nullable=False,
               postgresql_using="channel::text::contentchannelname")
    op.alter_column('posts', 'channel',
               existing_type=postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel'),
               type_=sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname'),
               existing_nullable=True,
               postgresql_using="channel::text::contentchannelname")

    op.execute("DROP TYPE postchannel")


def downgrade() -> None:
    op.execute("CREATE TYPE postchannel AS ENUM ('INSTAGRAM', 'LINKEDIN')")

    op.alter_column('posts', 'channel',
               existing_type=sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname'),
               type_=postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel'),
               existing_nullable=True,
               postgresql_using="channel::text::postchannel")
    op.alter_column('post_generation_jobs', 'channel',
               existing_type=sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname'),
               type_=postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel'),
               existing_nullable=False,
               postgresql_using="channel::text::postchannel")
    op.alter_column('campaigns', 'channels',
               existing_type=sa.ARRAY(sa.Enum('INSTAGRAM', 'LINKEDIN', name='contentchannelname')),
               type_=postgresql.ARRAY(postgresql.ENUM('INSTAGRAM', 'LINKEDIN', name='postchannel')),
               existing_nullable=True,
               postgresql_using="channels::text[]::postchannel[]")

    op.execute("DROP TYPE contentchannelname")

