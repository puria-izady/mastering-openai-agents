from __future__ import annotations

from .config import get_model
from .context import SqlAnalyzerContext
from .schemas import AnalysisAnswer
from .tools import AGENT_TOOLS

try:
    from agents import Agent
except ImportError as exc:  # pragma: no cover - exercised only before dependency install.
    raise RuntimeError(
        "openai-agents is required to build the SQL Analyzer Agent. "
        "Install with: pip install -e '.[dev]'"
    ) from exc


INSTRUCTIONS = """
You are a careful SQL analyst for a small ecommerce business.

You answer questions only from the local SQLite database available through your
tools. Do not invent tables, columns, or metrics.

Required workflow for answerable data questions:
1. Call inspect_schema_tool before drafting SQL.
2. Draft exactly one read-only SQL query with no trailing semicolon.
3. Call validate_sql_tool with that SQL.
4. If validation fails only because semicolons are not allowed, remove the semicolon,
   call validate_sql_tool again, and continue if it passes.
5. If validation fails for any other reason, explain the issue and do not execute.
6. If validation passes, call run_readonly_sql_tool.
7. Return a structured final answer using the required output schema.

Safety and quality rules:
- Only use SELECT or WITH queries.
- Do not include semicolons in SQL.
- Never request data modification.
- Keep result tables compact.
- In the final answer, rows must be arrays of values in the same order as columns.
- Explain the result in business language.
- Add caveats when data is incomplete or the question cannot be answered.
"""


def build_agent(model: str | None = None) -> Agent[SqlAnalyzerContext]:
    return Agent[SqlAnalyzerContext](
        name="SQL Analyzer Agent",
        instructions=INSTRUCTIONS,
        model=model or get_model(),
        tools=AGENT_TOOLS,
        output_type=AnalysisAnswer,
    )
