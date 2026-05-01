#!/usr/bin/env python3
"""
Push database schema changes directly to the database (equivalent to drizzle-kit push).
This creates/updates tables based on the current SQLAlchemy models without creating migration files.
"""

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine

from db.database import get_database_url
from db.schema_registry import Base


def main():
    print("Pushing database schema changes...")
    try:
        # Create a synchronous engine for schema operations
        # (create_all is a synchronous operation)
        database_url = get_database_url()
        # Ensure we're using the sync driver (postgresql:// not postgresql+asyncpg://)
        if database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace(
                "postgresql+asyncpg://", "postgresql://", 1
            )

        sync_engine = create_engine(database_url, echo=False)

        Base.metadata.create_all(sync_engine)
        sync_engine.dispose()
        print("✓ Database schema pushed successfully!")
    except Exception as e:
        print(f"✗ Error pushing schema: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
