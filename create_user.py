#!/usr/bin/env python3
"""Create a user in the Occurrences System.

Usage:
    python create_user.py <username> <password>
"""

import sys

from auth import create_user
from database import init_db

def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python create_user.py <username> <password>")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]
    init_db()

    if create_user(username, password):
        print(f"User '{username}' created successfully.")
    else:
        print(f"Error: user '{username}' already exists.")

if __name__ == "__main__":
    main()