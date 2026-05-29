# OpenAI Docs Verification

This reference solution was checked against the OpenAI docs through the OpenAI
docs MCP server on 2026-05-09 and refreshed for run-context guidance on
2026-05-13.

## Sources Checked

- [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [SDKs and CLI: Use the Agents SDK](https://developers.openai.com/api/docs/libraries#use-the-agents-sdk)
- [Using tools](https://developers.openai.com/api/docs/guides/tools#usage-in-the-agents-sdk)
- [Agent definitions: keep local context separate from model context](https://developers.openai.com/api/docs/guides/agents/define-agents#keep-local-context-separate-from-model-context)
- [Latest model guide](https://developers.openai.com/api/docs/guides/latest-model#using-reasoning-models)

## Implementation Mapping

| OpenAI docs guidance | Implementation |
|---|---|
| Define an `Agent`, run it with `Runner.run`, and inspect the returned result. | `src/sql_analyzer/agent.py` defines `build_agent`; `src/sql_analyzer/app.py` calls `Runner.run`. |
| Use the Agents SDK for code-first orchestration involving agents, tools, guardrails, tracing, or sandbox execution. | The app uses the Agents SDK rather than hand-rolling an LLM loop. |
| Add tools incrementally; Python function tools are a normal way to expose custom domain logic. | `src/sql_analyzer/tools.py` exposes schema inspection, SQL validation, and read-only SQL execution as function tools. |
| Use custom function tools for internal systems and domain-specific side effects. | Database access is exposed as custom tools because it is internal domain logic. |
| Pass application state and dependencies into a run without sending them to the model. | `agent.py` defines `Agent[SqlAnalyzerContext]`; `app.py` passes `SqlAnalyzerContext` to `Runner.run(..., context=...)`; database-backed tools receive `ctx: RunContextWrapper[SqlAnalyzerContext]`. |
| Put most tool-specific guidance in tool descriptions; use system instructions for workflow policy. | Tool docstrings describe tool purpose; `INSTRUCTIONS` defines required workflow and safety policy. |
| Use structured outputs for validation and accuracy where possible. | `AnalysisAnswer` is the agent `output_type`; it avoids open-ended `dict[str, Any]` fields so the SDK strict JSON schema validator accepts it. |
| Inspect traces early to debug model calls, tool calls, handoffs, and guardrails. | `app.py` wraps runs in `trace("sql-analyzer-agent")`; README directs you to the traces dashboard. |

## Deliberate Learning Choices

- The SQL validator is conservative. It rejects semicolons and database-control
  statements even when SQLite might technically allow a harmless variant.
- Tests focus on deterministic local behavior and skip API-backed checks unless
  `OPENAI_API_KEY` is present.
- The first lab uses only function tools. Hosted tools and handoffs belong in
  follow-up labs so you can see one capability boundary at a time.
