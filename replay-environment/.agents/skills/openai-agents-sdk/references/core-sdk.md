# Core SDK Patterns

Use `Agent` to define the model-facing specialist: name, instructions, model,
tools, handoffs, guardrails, sessions, and optional `output_type`.

Use `Runner.run(...)` for async execution and `Runner.run_streamed(...)` for
streaming. A run starts with a real SDK `Agent` or `SandboxAgent` and returns a
result with `final_output`, `new_items`, `last_agent`, usage data, and tracing
metadata.

Use `RunConfig` for per-run concerns:

- `workflow_name` for trace grouping.
- `trace_metadata` for course/lab identifiers.
- `model` or `model_settings` when overriding per-agent defaults.
- guardrails or handoff history settings when they are run-wide.
- `sandbox=SandboxRunConfig(...)` only for SandboxAgent runs.

Course reference pattern:

```python
from agents import Agent, RunConfig, Runner


def build_agent(model: str = "gpt-6-luna") -> Agent:
    return Agent(name="Assistant", instructions="Be precise.", model=model)


def build_run_config() -> RunConfig:
    return RunConfig(workflow_name="lab-example", trace_metadata={"lab": "example"})


async def run_demo(prompt: str) -> str:
    result = await Runner.run(build_agent(), prompt, run_config=build_run_config())
    return str(result.final_output)
```

Do not replace `Runner.run` with a custom framework runner.
