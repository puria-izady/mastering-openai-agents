# Build Log: Lab 01

## Prompts Used

- Prompt 1: first `Agent` plus `Runner.run`.
- Prompt 2: Pydantic `output_type`.
- Prompt 3: deterministic `@function_tool`.
- Prompt 4: input guardrail.
- Prompt 5: `SQLiteSession`.
- Prompt 6: shared `RunConfig`.

## Verification

- `uv run --with pytest pytest -q`: 6 passed.
- API-backed examples require `OPENAI_API_KEY`; local tests validate schemas,
  tools, guardrails, sessions, Agent construction, and RunConfig construction.
