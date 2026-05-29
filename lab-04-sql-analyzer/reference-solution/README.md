# SQL Analyzer Agent

Reference solution for a Codex-driven course lab in **Mastering OpenAI Agents**.

You use Codex to build a working OpenAI Agents SDK application that answers
business questions from a local SQLite database. The app demonstrates the core
difference between a chat-only LLM and an agent: the agent inspects a schema,
uses tools, validates SQL, executes a read-only query, and explains the result.

## What This Teaches

- `Agent`, `Runner.run`, and `RunResult`
- `RunContextWrapper` and local run context for application dependencies
- `RunConfig` for workflow and trace metadata
- Function tools with `@function_tool`
- Structured final output with Pydantic
- Strict JSON schema-compatible final output
- Tool descriptions as behavior contracts
- Read-only tool boundaries
- Agent trace inspection through the OpenAI platform
- Testable local logic around an API-backed agent

The implementation follows the current OpenAI docs guidance that the Agents SDK
is the right path for code-first orchestration involving agents, tools,
handoffs, guardrails, tracing, or sandbox execution:

- [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [SDKs and CLI: Use the Agents SDK](https://developers.openai.com/api/docs/libraries#use-the-agents-sdk)
- [Using tools](https://developers.openai.com/api/docs/guides/tools#usage-in-the-agents-sdk)
- [Keep local context separate from model context](https://developers.openai.com/api/docs/guides/agents/define-agents#keep-local-context-separate-from-model-context)

## Setup

```bash
cd "mastering-openai-agents/lab-04-sql-analyzer/reference-solution"
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env` and add your `OPENAI_API_KEY`.

## Seed The Database

```bash
python -m sql_analyzer.seed
```

This creates `data/ecommerce.db` with:

- customers
- products
- orders
- order_items
- refunds

## Run The Agent

```bash
sql-analyzer "Which products generated the most revenue?"
```

Or run the reference demo:

```bash
python run_reference.py
```

Example questions:

- `Which products generated the most revenue?`
- `What was total revenue by month?`
- `Which customers had refunds?`
- `What is the refund rate by product?`
- `Which product category has the highest average order value?`

After a run, open the [OpenAI traces dashboard](https://platform.openai.com/traces)
to inspect model calls, tool calls, and final output.

## Run Local Tests

```bash
pytest -q
```

The local tests cover database setup, schema inspection, SQL safety, and the
agent output contract. API-backed tests skip automatically when `OPENAI_API_KEY`
is not set.

## Run The Evaluation Set

```bash
sql-analyzer-eval
```

The eval runner includes deterministic local checks for SQL safety and optional
agent-backed questions when an API key is present.

## Architecture

```text
User question
    |
    v
Runner.run(context=SqlAnalyzerContext)
    |
    v
SQL Analyzer Agent
    |
    |-- inspect_schema_tool(ctx: RunContextWrapper)
    |
    |-- validate_sql_tool(sql)
    |
    |-- run_readonly_sql_tool(ctx: RunContextWrapper, sql)
    |
    v
DatabaseConnection
    |
    v
Structured AnalysisAnswer
    |
    |-- question
    |-- sql
    |-- columns
    |-- rows (value arrays matching columns)
    |-- explanation
    |-- caveats
```

## Safety Model

The system uses two layers:

1. Static SQL validation in `src/sql_analyzer/safety.py`
2. SQLite read-only mode plus an authorizer that blocks write operations during
   execution

This is intentionally conservative for a lab. Semicolons, non-`SELECT`
statements, write keywords, and suspicious database-control commands are
rejected.
