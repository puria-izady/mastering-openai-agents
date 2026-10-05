# Build Log: Lab 04

## Prompts Used

- Source prompt pack: `prompt-pack.md`.
- Course alignment prompt: verify SDK-first structure, read-only SQL tools,
  structured output, optional API-backed execution, and Markdown materials.

## Verification

- OpenAI docs verification recorded in `docs/openai-docs-verification.md`.
- Reference implementation moved into this Lab 04 `reference-solution/`
  folder so the lab structure matches the rest of the course.
- Added explicit `build_run_config()` and passed it into `Runner.run(...)`.
- Refactored database access into SDK run context:
  `Runner.run(..., context=SqlAnalyzerContext(...))`, with database-backed
  tools receiving `ctx: RunContextWrapper[SqlAnalyzerContext]`.
- Updated prompt pack so recreating Lab 04 asks for run-context dependency
  injection instead of environment mutation.
- Fixed `AnalysisAnswer` to be strict JSON schema compatible by replacing
  open-ended `dict[str, Any]` final rows with ordered value arrays matching the
  `columns` field.
- Verification: `uv run pytest -q` -> 17 passed, 1 skipped.


## 2026-10-05 — GPT-6 Luna default update

Updated text/sandbox agent defaults to `gpt-6-luna` and verified SDK model
contracts locally. Explicit model overrides remain available; dedicated
transcription, speech, and realtime models are unchanged.

Local pytest suite: **19 passed, 1 skipped**, using openai-agents 0.17.3.
API credentials were removed from the test environment. No live model calls
were made; this verifies configuration and local behavior, not live API access.
No-key demo check: printed the existing credential requirement and exited 1.
SQL eval: all five local safety checks passed; agent checks skipped without a key.
