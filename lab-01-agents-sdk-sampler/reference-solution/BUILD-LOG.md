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


## 2026-10-05 — GPT-6 Luna default update

Updated text/sandbox agent defaults to `gpt-6-luna` and verified SDK model
contracts locally. Explicit model overrides remain available; dedicated
transcription, speech, and realtime models are unchanged.

Local pytest suite: **7 passed, 1 skipped**, using openai-agents 0.17.3.
API credentials were removed from the test environment. No live model calls
were made; this verifies configuration and local behavior, not live API access.
No-key demo check: printed the existing credential requirement and exited 1.
