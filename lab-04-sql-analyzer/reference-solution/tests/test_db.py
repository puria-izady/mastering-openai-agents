from pathlib import Path

import pytest

from sql_analyzer.db import initialize_database, inspect_schema, run_readonly_query


@pytest.fixture()
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "ecommerce.db"
    initialize_database(path)
    return path


def test_seed_creates_expected_schema(db_path: Path) -> None:
    schema = inspect_schema(db_path)
    table_names = {table.name for table in schema.tables}
    assert {"customers", "orders", "order_items", "products", "refunds"}.issubset(table_names)


def test_schema_contains_descriptions(db_path: Path) -> None:
    schema = inspect_schema(db_path)
    products = next(table for table in schema.tables if table.name == "products")
    assert products.description
    assert any(column.name == "unit_price" and column.description for column in products.columns)


def test_run_readonly_query_returns_rows(db_path: Path) -> None:
    result = run_readonly_query(
        """
        SELECT p.name, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.name
        ORDER BY revenue DESC
        """,
        db_path,
    )
    assert result.columns == ["name", "revenue"]
    assert result.rows
    assert result.rows[0]["revenue"] > 0


def test_run_readonly_query_rejects_writes(db_path: Path) -> None:
    with pytest.raises(ValueError):
        run_readonly_query("DELETE FROM products", db_path)


def test_run_readonly_query_truncates(db_path: Path) -> None:
    result = run_readonly_query("SELECT name FROM products ORDER BY name", db_path, max_rows=2)
    assert result.row_count == 2
    assert result.truncated is True

