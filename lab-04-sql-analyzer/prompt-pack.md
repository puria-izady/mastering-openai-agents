# Prompt Pack: Recreate the SQL Analyzer Agent with Codex

Use these prompts in sequence from an empty workspace.

## Prompt 1: Scaffold

```text
Create a Python project for a course lab called sql-analyzer-agent.

The app should become a small SQL Analyzer Agent, but do not call the OpenAI API
yet. First create the project skeleton, a seedable ecommerce SQLite database,
local database utilities, tests, README.md, and .env.example.

Use a src/ package layout. Add customers, products, orders, order_items, and
refunds tables. Add tests proving the database can be seeded and inspected.

Before editing, inspect the workspace and propose the file structure. Then
create the files and run the tests.
```

## Prompt 2: Safety

```text
Add a conservative read-only SQL safety layer.

Requirements:
- Allow SELECT and WITH queries.
- Reject INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, REPLACE, VACUUM, ATTACH,
  DETACH, PRAGMA, and semicolons.
- Ignore unsafe words inside string literals and comments.
- Add a SQLite authorizer for execution-time write protection.
- Add focused tests for accepted and rejected SQL.

Run the tests and summarize the behavior.
```

## Prompt 3: Function Tools

```text
Expose the local SQL Analyzer capabilities as OpenAI Agents SDK function tools.

Add:
- inspect_schema_tool()
- validate_sql_tool(sql)
- run_readonly_sql_tool(sql, max_rows=25)

Add a typed run context object that contains the database dependency. Tools
that need the database must receive `RunContextWrapper[SqlAnalyzerContext]` as
the first argument named `ctx` and read the database from `ctx.context`. Do not rely on
environment mutation or module-level global database state for tool execution.

Keep implementation functions separately callable so tests can run without an
OpenAI API key. Add tests for the implementation functions and for the fact
that the tool schema does not expose the run-context argument to the model.
```

## Prompt 4: Agent

```text
Create the OpenAI Agents SDK agent.

Requirements:
- Use Agent and Runner.run from the Agents SDK.
- Type the agent as `Agent[SqlAnalyzerContext]`.
- Use @function_tool tools from the previous step.
- Pass the database dependency with `Runner.run(..., context=...)`.
- Keep `RunConfig` visible with workflow_name and trace_metadata.
- Use a Pydantic structured output model called AnalysisAnswer.
- Make `AnalysisAnswer` strict JSON schema compatible for the Agents SDK. Do not
  use `dict[str, Any]` in the final output model. Represent result rows as
  `list[list[str | int | float | bool | None]]`, with values in the same order
  as the `columns` array.
- The agent must inspect the schema before writing SQL.
- It must validate SQL before execution.
- It must draft SQL without semicolons. If validation fails only because a
  semicolon was included, it must remove the semicolon, validate again, and then
  execute only after validation passes.
- It must explain the result in business language and include caveats.
- Add a CLI entrypoint: sql-analyzer "question".
- API-backed tests should skip cleanly if OPENAI_API_KEY is missing.
- Add a local test that constructs `AgentOutputSchema(AnalysisAnswer)` so
  strict schema issues are caught before a real model run.

Run tests after implementation.
```

## Prompt 5: Evals And Lab Materials

```text
Add a small eval runner and course materials.

Create Markdown files only for course content:
- lab-guide.md
- discussion-guide.md
- verification-checklist.md
- prompt-pack.md

Add an eval command that runs local SQL safety checks without an API key and
agent-backed checks when OPENAI_API_KEY is available.

Run tests and the eval command.
```
