#!/usr/bin/env python3

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from alembic import command
from alembic.config import Config


def main():
    print("Applying database migrations...")  # noqa: T201

    backend_dir = Path(__file__).parent.parent.parent
    alembic_cfg = Config(backend_dir / "alembic.ini")

    try:
        command.upgrade(alembic_cfg, "head")
        print("✓ Migrations applied successfully!")  # noqa: T201
        return 0
    except Exception as e:
        print(f"✗ Error applying migrations: {e}", file=sys.stderr)  # noqa: T201
        return 1


if __name__ == "__main__":
    main()
