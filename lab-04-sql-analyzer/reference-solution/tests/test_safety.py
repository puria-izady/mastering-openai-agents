from sql_analyzer.safety import validate_readonly_sql


def assert_rejected(sql: str) -> None:
    result = validate_readonly_sql(sql)
    assert not result.ok, result.reason


def test_select_and_with_are_allowed() -> None:
    assert validate_readonly_sql("SELECT name FROM products").ok
    assert validate_readonly_sql("WITH totals AS (SELECT 1 AS n) SELECT n FROM totals").ok


def test_empty_sql_is_rejected() -> None:
    assert_rejected("")


def test_non_select_statements_are_rejected() -> None:
    for sql in [
        "INSERT INTO products(name) VALUES ('x')",
        "UPDATE products SET name = 'x'",
        "DELETE FROM products",
        "DROP TABLE products",
        "ALTER TABLE products ADD COLUMN x TEXT",
        "CREATE TABLE x(id INTEGER)",
        "VACUUM",
        "PRAGMA table_info(products)",
    ]:
        assert_rejected(sql)


def test_multiple_statements_are_rejected() -> None:
    assert_rejected("SELECT 1; SELECT 2")


def test_mutation_words_inside_strings_do_not_trigger() -> None:
    result = validate_readonly_sql("SELECT 'delete' AS word FROM products")
    assert result.ok


def test_mutation_words_inside_comments_do_not_trigger() -> None:
    result = validate_readonly_sql("SELECT name FROM products -- delete later")
    assert result.ok

