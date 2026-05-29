from __future__ import annotations

from .config import get_db_path
from .db import initialize_database


def main() -> None:
    db_path = initialize_database(get_db_path())
    print(f"Seeded database at {db_path}")


if __name__ == "__main__":
    main()

