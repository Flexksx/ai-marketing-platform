#!/usr/bin/env python3

import sys

from db.scripts.db_generate import main as db_main


def main():
    if len(sys.argv) < 2:
        sys.argv.append("Auto-generated migration")
    return db_main()


if __name__ == "__main__":
    sys.exit(main() or 0)
