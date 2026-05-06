#!/usr/bin/env python3
import os
import subprocess
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def main():
    print("Formatting Python backend code...")

    os.chdir(backend_dir)

    try:
        print("Running ruff check --fix...")
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--fix", "."],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)
        print("✓ ruff check completed successfully!")

        print("Running ruff format...")
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "format", "."],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)
        print("✓ ruff format completed successfully!")

        print("✓ Formatting completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"✗ Error during formatting: {e}", file=sys.stderr)
        if e.stdout:
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
