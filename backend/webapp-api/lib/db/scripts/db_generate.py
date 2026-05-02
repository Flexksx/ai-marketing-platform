#!/usr/bin/env python3

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from alembic.config import Config

from alembic import command


def main():
    if len(sys.argv) < 2:
        print("Usage: db-generate <migration_message>", file=sys.stderr)
        print("Example: db-generate 'add user table'", file=sys.stderr)
        return 1

    message = sys.argv[1]
    print(f"Generating migration: {message}...")

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))

    try:
        command.revision(alembic_cfg, autogenerate=True, message=message)
        print("✓ Migration generated successfully!")
        return 0
    except Exception as e:
        print(f"✗ Error generating migration: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()
