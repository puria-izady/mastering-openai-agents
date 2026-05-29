# Prompt 3: Function Tools

Expose the local SQL Analyzer capabilities as OpenAI Agents SDK function tools.

Add:

- `inspect_schema_tool()`
- `validate_sql_tool(sql)`
- `run_readonly_sql_tool(sql, max_rows=25)`

Add a typed run context object that contains the database dependency. Tools
that need the database must receive `RunContextWrapper[SqlAnalyzerContext]` as
the first argument named `ctx` and read the database from `ctx.context`. Do not rely on
environment mutation or module-level global database state for tool execution.

Keep implementation functions separately callable so tests can run without an
OpenAI API key. Add tests for the implementation functions and for the fact
that the tool schema does not expose the run-context argument to the model.
