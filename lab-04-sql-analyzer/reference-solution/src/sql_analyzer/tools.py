from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

from .context import SqlAnalyzerContext
from .safety import validate_readonly_sql

try:
    from agents import RunContextWrapper, function_tool
except ImportError:  # Keeps local tests runnable before installing openai-agents.
    F = TypeVar("F", bound=Callable[..., Any])
    T = TypeVar("T")

    class RunContextWrapper(Generic[T]):
        def __init__(self, context: T) -> None:
            self.context = context

    def function_tool(func: F) -> F:
        return func


def inspect_schema_impl(context: SqlAnalyzerContext) -> dict[str, Any]:
    schema = context.database.inspect_schema()
    return schema.model_dump()


def validate_sql_impl(sql: str) -> dict[str, Any]:
    validation = validate_readonly_sql(sql)
    return validation.model_dump()


def run_readonly_sql_impl(context: SqlAnalyzerContext, sql: str, max_rows: int = 25) -> dict[str, Any]:
    result = context.database.run_readonly_sql(sql, max_rows=max_rows)
    return result.model_dump()


@function_tool
def inspect_schema_tool(ctx: RunContextWrapper[SqlAnalyzerContext]) -> dict[str, Any]:
    """Inspect the local ecommerce SQLite schema before writing SQL."""
    return inspect_schema_impl(ctx.context)


@function_tool
def validate_sql_tool(sql: str) -> dict[str, Any]:
    """Validate that SQL is a conservative read-only SELECT/WITH query with no semicolon."""
    return validate_sql_impl(sql)


@function_tool
def run_readonly_sql_tool(
    ctx: RunContextWrapper[SqlAnalyzerContext],
    sql: str,
    max_rows: int = 25,
) -> dict[str, Any]:
    """Execute already-validated read-only SQL against the ecommerce database."""
    return run_readonly_sql_impl(ctx.context, sql, max_rows=max_rows)


AGENT_TOOLS = [inspect_schema_tool, validate_sql_tool, run_readonly_sql_tool]
