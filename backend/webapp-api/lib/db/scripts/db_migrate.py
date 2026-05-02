#!/usr/bin/env python3

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from alembic.config import Config

from alembic import command


def main():
    print("Applying database migrations...")

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))

    try:
        command.upgrade(alembic_cfg, "head")
        print("✓ Migrations applied successfully!")
        return 0
    except Exception as e:
        print(f"✗ Error applying migrations: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()
