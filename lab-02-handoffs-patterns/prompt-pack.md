# Prompt Pack: Lab 02

Use these prompts in order. Both variants must use real OpenAI Agents SDK
objects directly: `Agent(... handoffs=[...])` and `specialist.as_tool(...)`.
Every runnable path must pass a shared `RunConfig`.

## Prompt 1

```text
Create a customer-support triage project using the OpenAI Agents SDK.

Build a triage agent, billing specialist, and technical specialist using
handoffs. Add runnable examples for three prompts and pass RunConfig into
Runner.run.
```

## Prompt 2

```text
Add logging that prints final_output and last_agent.name for each run.

Add README guidance telling you to inspect the OpenAI traces dashboard.
```

## Prompt 3

```text
Create a second implementation where the manager calls specialists with
agent.as_tool instead of handoffs.

Keep the same scenarios so you can compare behavior. The runner must print
the manager final output, result.last_agent.name, and the captured tool outputs
from SDK run items so you can see what each specialist returned.
```

## Prompt 4

```text
Create a Markdown worksheet that asks you to compare ownership, trace
shape, and final response quality between handoffs and agents-as-tools.
```

## Prompt 5

```text
Add build_run_config for the lab and tests that verify:
- the handoff manager has real SDK handoffs
- the agents-as-tools manager exposes specialist tools from Agent.as_tool
- both runnable variants call Runner.run with RunConfig
- the agents-as-tools runner can display captured tool outputs and last_agent
```
