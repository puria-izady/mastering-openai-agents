# Prompt 4: Agent

Create the OpenAI Agents SDK agent.

Requirements:

- Use `Agent` and `Runner.run` from the Agents SDK.
- Type the agent as `Agent[SqlAnalyzerContext]`.
- Use `@function_tool` tools from the previous step.
- Pass the database dependency with `Runner.run(..., context=...)`.
- Keep `RunConfig` visible with `workflow_name` and `trace_metadata`.
- Use a Pydantic structured output model called `AnalysisAnswer`.
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
- Add a CLI entrypoint: `sql-analyzer "question"`.
- API-backed tests should skip cleanly if `OPENAI_API_KEY` is missing.
- Add a local test that constructs `AgentOutputSchema(AnalysisAnswer)` so
  strict schema issues are caught before a real model run.

Run tests after implementation.
