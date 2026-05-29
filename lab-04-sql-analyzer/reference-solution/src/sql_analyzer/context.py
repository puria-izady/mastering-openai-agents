from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import get_db_path
from .db import initialize_database, inspect_schema, run_readonly_query
from .schemas import QueryResult, SchemaInfo


@dataclass(frozen=True)
class DatabaseConnection:
    path: Path

    @classmethod
    def from_path(cls, path: Path | str | None = None) -> DatabaseConnection:
        db_path = Path(path).expanduser().resolve() if path is not None else get_db_path()
        return cls(path=db_path)

    def ensure_initialized(self) -> None:
        if not self.path.exists():
            initialize_database(self.path)

    def inspect_schema(self) -> SchemaInfo:
        return inspect_schema(self.path)

    def run_readonly_sql(self, sql: str, *, max_rows: int = 25) -> QueryResult:
        return run_readonly_query(sql, self.path, max_rows=max_rows)


@dataclass(frozen=True)
class SqlAnalyzerContext:
    database: DatabaseConnection


def build_context(db_path: Path | str | None = None) -> SqlAnalyzerContext:
    database = DatabaseConnection.from_path(db_path)
    database.ensure_initialized()
    return SqlAnalyzerContext(database=database)
