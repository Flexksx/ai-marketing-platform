#!/usr/bin/env python3
"""
Reset database - drops all tables and recreates them (use with caution!).
Equivalent to dropping and recreating the database schema.
"""

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine

from lib.db.database import get_database_url
from lib.db.schema_registry import Base


def main():
    confirm = input("⚠️  This will DROP ALL TABLES. Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("Aborted.")
        sys.exit(0)

    print("Dropping all tables...")
    sync_engine = create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )
    try:
        Base.metadata.drop_all(sync_engine)
        print("✓ All tables dropped.")

        print("Creating tables from schema...")
        Base.metadata.create_all(sync_engine)
        print("✓ Database reset successfully!")
    except Exception as e:
        print(f"✗ Error resetting database: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
