# Testing Patterns

Every lab reference should have tests that run without `OPENAI_API_KEY`.

Use local tests for:

- Pydantic schemas.
- deterministic tool implementations.
- policy and retrieval helpers.
- `Agent` and `SandboxAgent` object construction.
- `RunConfig` construction.
- tool, handoff, guardrail, and session contracts.

Use API-backed smoke tests only when valuable. Mark them skipped when
`OPENAI_API_KEY` is absent.

Useful SDK contract assertions:

```python
from agents import Agent, RunConfig

agent = build_agent()
assert isinstance(agent, Agent)
assert len(agent.tools) > 0

run_config = build_run_config()
assert isinstance(run_config, RunConfig)
assert run_config.workflow_name
```

Do not assert exact model prose. Assert structure, tool availability, routing
contracts, and deterministic local behavior.
