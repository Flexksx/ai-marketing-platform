#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))


def main():
    print("Formatting Python backend code...")  # noqa: T201

    os.chdir(backend_dir)

    try:
        print("Running ruff check --fix...")  # noqa: T201
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--fix", "."],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)  # noqa: T201
        print("✓ ruff check completed successfully!")  # noqa: T201

        print("Running ruff format...")  # noqa: T201
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "format", "."],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)  # noqa: T201
        print("✓ ruff format completed successfully!")  # noqa: T201

        print("✓ Formatting completed successfully!")  # noqa: T201

    except subprocess.CalledProcessError as e:
        print(f"✗ Error during formatting: {e}", file=sys.stderr)  # noqa: T201
        if e.stdout:
            print(e.stdout, file=sys.stderr)  # noqa: T201
        if e.stderr:
            print(e.stderr, file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
