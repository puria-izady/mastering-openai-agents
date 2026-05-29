# Lab Guide: Build a SQL Analyzer Agent with Codex

## Objective

Use Codex to build an OpenAI Agents SDK application that answers business
questions from a local SQLite database.

By the end of the lab, you will have built:

- A seeded ecommerce SQLite database
- Function tools for schema inspection, SQL validation, and read-only execution
- An OpenAI `Agent` with structured output
- SDK run context that carries the database dependency into tools
- A CLI for asking one business question
- Tests for local database and SQL safety behavior
- A small eval runner

## Time Estimate

60-75 minutes.

## Prerequisites

- Python 3.11+
- OpenAI API key
- Basic SQL knowledge
- Codex available in the project workspace

## Learning Outcomes

You will be able to:

- Explain why this is an agent rather than a single model call.
- Use Codex to scaffold a focused Agents SDK project.
- Create Python function tools for domain logic.
- Pass local application dependencies through SDK run context.
- Validate tool inputs before executing sensitive operations.
- Use structured final outputs.
- Design structured outputs that satisfy the Agents SDK strict JSON schema.
- Run tests and inspect traces.

## Part 1: Scaffold the Project

Ask Codex to create a Python project named `sql-analyzer-agent`.

Checkpoint:

- `pyproject.toml` exists.
- `src/sql_analyzer/` exists.
- `tests/` exists.
- `README.md` explains setup and usage.

## Part 2: Create the Database

Ask Codex to create an ecommerce SQLite database with customers, products,
orders, order items, and refunds.

Checkpoint:

- `python -m sql_analyzer.seed` creates `data/ecommerce.db`.
- A local test proves the expected tables exist.

## Part 3: Add SQL Safety

Ask Codex to add a conservative read-only SQL validator.

Checkpoint:

- `SELECT` and `WITH` pass.
- `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `PRAGMA`, and semicolons fail.
- Tests cover accepted and rejected SQL.

## Part 4: Add Agent Tools

Ask Codex to expose three function tools:

- `inspect_schema_tool`
- `validate_sql_tool`
- `run_readonly_sql_tool`

Checkpoint:

- Tools work through local implementation functions.
- Database-backed tools receive `ctx: RunContextWrapper[SqlAnalyzerContext]`.
- Tool schemas do not expose the run-context argument to the model.
- Tool descriptions are specific enough for the model to choose correctly.

## Part 5: Build the Agent

Ask Codex to create an OpenAI Agents SDK `Agent` that:

- Calls schema inspection before writing SQL
- Validates SQL before execution
- Executes only through the read-only tool
- Calls `Runner.run(..., context=...)` with the database dependency
- Returns a strict-schema-compatible `AnalysisAnswer`

Checkpoint:

- `sql-analyzer "Which products generated the most revenue?"` returns SQL,
  columns, value-array rows, explanation, and caveats.
- The OpenAI traces dashboard shows model and tool calls.

## Part 6: Add Evals

Ask Codex to add a small eval runner.

Checkpoint:

- Local safety checks run without an API key.
- Agent-backed checks run when `OPENAI_API_KEY` is present.

## Troubleshooting

| Problem | Fix |
|---|---|
| `OPENAI_API_KEY` missing | Copy `.env.example` to `.env` and add the key. |
| Database file missing | Run `python -m sql_analyzer.seed`. |
| Import errors | Run `pip install -e ".[dev]"` from the lab folder. |
| Agent writes unsafe SQL | Strengthen the instructions and add a safety test. |
| Query cannot answer question | Add a caveat instead of inventing missing data. |

## Extension Challenges

- Add a query classification step: answerable, ambiguous, unsupported, unsafe.
- Add a clarification flow for ambiguous questions.
- Add a second specialist agent for business interpretation.
- Add a document policy tool and answer questions that combine SQL and policy.
- Add a human approval pause before expensive or sensitive queries.
