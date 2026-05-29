from pathlib import Path

from sql_analyzer.context import build_context
from sql_analyzer.db import initialize_database
from sql_analyzer.tools import inspect_schema_impl, run_readonly_sql_impl, validate_sql_impl


def test_tool_impls_work_without_openai_agents_runtime(tmp_path: Path) -> None:
    db_path = tmp_path / "ecommerce.db"
    initialize_database(db_path)
    context = build_context(db_path)

    schema = inspect_schema_impl(context)
    assert any(table["name"] == "orders" for table in schema["tables"])

    validation = validate_sql_impl("SELECT COUNT(*) AS n FROM orders")
    assert validation["ok"] is True

    result = run_readonly_sql_impl(context, "SELECT COUNT(*) AS n FROM orders")
    assert result["rows"][0]["n"] == 8


def test_context_chooses_database_without_mutating_environment(monkeypatch, tmp_path: Path) -> None:
    env_db = tmp_path / "env.db"
    explicit_db = tmp_path / "explicit.db"
    monkeypatch.setenv("SQL_ANALYZER_DB_PATH", str(env_db))

    context = build_context(explicit_db)

    assert context.database.path == explicit_db.resolve()
    assert explicit_db.exists()
    assert not env_db.exists()
