#!/usr/bin/env python3
"""
Reset database - drops all tables and recreates them (use with caution!).
Equivalent to dropping and recreating the database schema.
"""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine

from lib.db.database import get_database_url
from lib.db.schema_registry import Base


def main():
    confirm = input("⚠️  This will DROP ALL TABLES. Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("Aborted.")  # noqa: T201
        sys.exit(0)

    print("Dropping all tables...")  # noqa: T201
    sync_engine = create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )
    try:
        Base.metadata.drop_all(sync_engine)
        print("✓ All tables dropped.")  # noqa: T201

        print("Creating tables from schema...")  # noqa: T201
        Base.metadata.create_all(sync_engine)
        print("✓ Database reset successfully!")  # noqa: T201
    except Exception as e:
        print(f"✗ Error resetting database: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
