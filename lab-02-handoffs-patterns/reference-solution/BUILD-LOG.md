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
