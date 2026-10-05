# Build Log: Lab 02

## Prompts Used

- Prompt 1: handoff triage with billing and technical specialists.
- Prompt 2: result logging with `final_output` and `last_agent.name`.
- Prompt 3: agents-as-tools manager with `Agent.as_tool`, visible tool outputs,
  and `last_agent`.
- Prompt 4: trace comparison worksheet.
- Prompt 5: shared `RunConfig` and orchestration contract tests.

## Verification

- `uv run --with pytest pytest -q`: 5 passed.
- Tests validate real SDK handoffs, agents-as-tools, scenarios, and RunConfig.


## 2026-10-05 — GPT-6 Luna default update

Updated text/sandbox agent defaults to `gpt-6-luna` and verified SDK model
contracts locally. Explicit model overrides remain available; dedicated
transcription, speech, and realtime models are unchanged.

Local pytest suite: **7 passed, 2 skipped**, using openai-agents 0.17.3.
API credentials were removed from the test environment. No live model calls
were made; this verifies configuration and local behavior, not live API access.
No-key demo check: printed the existing credential requirement and exited 1.
