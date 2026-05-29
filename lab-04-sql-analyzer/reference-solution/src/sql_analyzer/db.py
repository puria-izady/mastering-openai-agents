from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .config import get_db_path
from .safety import readonly_authorizer, validate_readonly_sql
from .schemas import ColumnInfo, QueryResult, SchemaInfo, TableInfo


TABLE_DESCRIPTIONS = {
    "customers": "People who placed orders in the store.",
    "products": "Sellable products with category and unit price.",
    "orders": "Order headers with customer, date, status, and channel.",
    "order_items": "Line items connecting orders to products and quantities.",
    "refunds": "Refund events linked to orders and optionally products.",
}

COLUMN_DESCRIPTIONS = {
    "customers.customer_id": "Primary key for a customer.",
    "customers.name": "Customer full name.",
    "customers.segment": "Business segment such as consumer, SMB, or enterprise.",
    "customers.region": "Customer region.",
    "products.product_id": "Primary key for a product.",
    "products.name": "Product name.",
    "products.category": "Product category.",
    "products.unit_price": "Current listed unit price in USD.",
    "orders.order_id": "Primary key for an order.",
    "orders.customer_id": "Customer who placed the order.",
    "orders.order_date": "ISO date when the order was placed.",
    "orders.status": "Order lifecycle status.",
    "orders.channel": "Sales channel.",
    "order_items.order_item_id": "Primary key for an order line.",
    "order_items.order_id": "Order that owns the line item.",
    "order_items.product_id": "Product sold on this line.",
    "order_items.quantity": "Units sold.",
    "order_items.unit_price": "Price charged per unit in USD.",
    "refunds.refund_id": "Primary key for a refund.",
    "refunds.order_id": "Refunded order.",
    "refunds.product_id": "Refunded product when the refund is product-specific.",
    "refunds.refund_date": "ISO date when the refund was issued.",
    "refunds.amount": "Refund amount in USD.",
    "refunds.reason": "Business reason for the refund.",
}


def connect(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def connect_readonly(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or get_db_path()
    uri = f"file:{db_path.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.set_authorizer(readonly_authorizer)
    return conn


def connect_readonly_schema(path: Path | None = None) -> sqlite3.Connection:
    db_path = path or get_db_path()
    uri = f"file:{db_path.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(path: Path | None = None) -> Path:
    db_path = path or get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with connect(db_path) as conn:
        conn.executescript(
            """
            DROP TABLE IF EXISTS refunds;
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS customers;

            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                segment TEXT NOT NULL,
                region TEXT NOT NULL
            );

            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                unit_price REAL NOT NULL
            );

            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
                channel TEXT NOT NULL
            );

            CREATE TABLE order_items (
                order_item_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER NOT NULL REFERENCES products(product_id),
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL
            );

            CREATE TABLE refunds (
                refund_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER REFERENCES products(product_id),
                refund_date TEXT NOT NULL,
                amount REAL NOT NULL,
                reason TEXT NOT NULL
            );
            """
        )

        conn.executemany(
            "INSERT INTO customers(customer_id, name, segment, region) VALUES (?, ?, ?, ?)",
            [
                (1, "Ada Chen", "enterprise", "North America"),
                (2, "Bruno Silva", "smb", "Europe"),
                (3, "Carla Meyer", "consumer", "Europe"),
                (4, "Dev Patel", "enterprise", "Asia-Pacific"),
                (5, "Elena Rossi", "smb", "Europe"),
                (6, "Fatima Khan", "consumer", "North America"),
            ],
        )
        conn.executemany(
            "INSERT INTO products(product_id, name, category, unit_price) VALUES (?, ?, ?, ?)",
            [
                (1, "Analytics Pro", "software", 199.0),
                (2, "Automation Pack", "software", 149.0),
                (3, "Team Training", "services", 499.0),
                (4, "Support Plus", "services", 299.0),
                (5, "Data Connector", "software", 99.0),
            ],
        )
        conn.executemany(
            "INSERT INTO orders(order_id, customer_id, order_date, status, channel) VALUES (?, ?, ?, ?, ?)",
            [
                (101, 1, "2026-01-12", "paid", "sales"),
                (102, 2, "2026-01-20", "paid", "self-serve"),
                (103, 3, "2026-02-03", "paid", "self-serve"),
                (104, 4, "2026-02-18", "paid", "sales"),
                (105, 5, "2026-03-02", "paid", "partner"),
                (106, 6, "2026-03-15", "paid", "self-serve"),
                (107, 1, "2026-04-04", "paid", "sales"),
                (108, 2, "2026-04-16", "paid", "self-serve"),
            ],
        )
        conn.executemany(
            "INSERT INTO order_items(order_item_id, order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?, ?)",
            [
                (1001, 101, 1, 4, 199.0),
                (1002, 101, 3, 1, 499.0),
                (1003, 102, 2, 2, 149.0),
                (1004, 102, 5, 5, 99.0),
                (1005, 103, 1, 1, 199.0),
                (1006, 103, 4, 1, 299.0),
                (1007, 104, 1, 5, 199.0),
                (1008, 104, 2, 3, 149.0),
                (1009, 105, 3, 2, 499.0),
                (1010, 106, 5, 2, 99.0),
                (1011, 107, 4, 3, 299.0),
                (1012, 108, 2, 1, 149.0),
                (1013, 108, 5, 1, 99.0),
            ],
        )
        conn.executemany(
            "INSERT INTO refunds(refund_id, order_id, product_id, refund_date, amount, reason) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (501, 102, 5, "2026-01-25", 99.0, "duplicate connector"),
                (502, 103, 4, "2026-02-09", 149.5, "support expectation mismatch"),
                (503, 108, 2, "2026-04-20", 149.0, "changed plan"),
            ],
        )

    return db_path


def inspect_schema(path: Path | None = None) -> SchemaInfo:
    with connect_readonly_schema(path) as conn:
        table_rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        tables: list[TableInfo] = []
        for row in table_rows:
            table_name = row["name"]
            columns = []
            for col in conn.execute(f"PRAGMA table_info({table_name})").fetchall():
                key = f"{table_name}.{col['name']}"
                columns.append(
                    ColumnInfo(
                        name=col["name"],
                        type=col["type"],
                        nullable=not bool(col["notnull"]),
                        primary_key=bool(col["pk"]),
                        description=COLUMN_DESCRIPTIONS.get(key, ""),
                    )
                )
            tables.append(
                TableInfo(
                    name=table_name,
                    description=TABLE_DESCRIPTIONS.get(table_name, ""),
                    columns=columns,
                )
            )
        return SchemaInfo(tables=tables)


def run_readonly_query(sql: str, path: Path | None = None, max_rows: int = 25) -> QueryResult:
    validation = validate_readonly_sql(sql)
    if not validation.ok:
        raise ValueError(validation.reason)

    with connect_readonly(path) as conn:
        cursor = conn.execute(sql)
        rows = cursor.fetchmany(max_rows + 1)
        truncated = len(rows) > max_rows
        rows = rows[:max_rows]
        columns = [description[0] for description in cursor.description or []]
        data: list[dict[str, Any]] = [dict(row) for row in rows]

    return QueryResult(
        sql=sql,
        columns=columns,
        rows=data,
        row_count=len(data),
        truncated=truncated,
    )
