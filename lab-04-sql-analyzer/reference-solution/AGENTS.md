# AGENTS.md

You are working in the `sql-analyzer-agent` reference solution for the course
Mastering OpenAI Agents.

## Course constraints

- Create course-facing content as Markdown, not PPTX.
- Keep the lab focused on OpenAI Agents SDK primitives.
- Prefer small, inspectable code over clever abstractions.

## Commands

- Seed the database: `python -m sql_analyzer.seed`
- Run tests: `pytest -q`
- Run one question: `sql-analyzer "Which products generated the most revenue?"`
- Run evals: `sql-analyzer-eval`

## Safety rules

- SQL execution must remain read-only.
- Do not weaken `safety.py` without adding tests for the new behavior.
- Tests must pass without an OpenAI API key. API-backed tests should skip cleanly.

