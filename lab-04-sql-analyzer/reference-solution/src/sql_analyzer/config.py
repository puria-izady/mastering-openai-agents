from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "ecommerce.db"


def get_model() -> str:
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-5.5")


def get_db_path() -> Path:
    raw = os.getenv("SQL_ANALYZER_DB_PATH")
    if not raw:
        return DEFAULT_DB_PATH

    path = Path(raw).expanduser()
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path

