#!/usr/bin/env python3

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from alembic import command
from alembic.config import Config


def main():
    if len(sys.argv) < 2:
        print("Usage: db-generate <migration_message>", file=sys.stderr)  # noqa: T201
        print("Example: db-generate 'add user table'", file=sys.stderr)  # noqa: T201
        return 1

    message = sys.argv[1]
    print(f"Generating migration: {message}...")  # noqa: T201

    backend_dir = Path(__file__).parent.parent.parent
    alembic_cfg = Config(backend_dir / "alembic.ini")

    try:
        command.revision(alembic_cfg, autogenerate=True, message=message)
        print("✓ Migration generated successfully!")  # noqa: T201
        return 0
    except Exception as e:
        print(f"✗ Error generating migration: {e}", file=sys.stderr)  # noqa: T201
        return 1


if __name__ == "__main__":
    main()
