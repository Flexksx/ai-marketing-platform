#!/usr/bin/env python3

import sys

from db.scripts.db_migrate import main as db_main


def main():
    return db_main()


if __name__ == "__main__":
    sys.exit(main() or 0)
