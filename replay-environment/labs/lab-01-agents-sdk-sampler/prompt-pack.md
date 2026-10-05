# Prompt Pack: Lab 01

Default all SDK Agent/SandboxAgent model settings to `gpt-6-luna`. Keep modality-specific transcription, speech, and realtime audio model IDs unchanged.

Use these prompts in order. The reference must use direct OpenAI Agents SDK
objects, not course abstractions. Add `build_run_config()` and pass the returned
`RunConfig` into every runnable `Runner.run(...)` example.

## Prompt 1

```text
Create an agents-sdk-sampler Python project.

Add one runnable example that defines an Agent, runs it with Runner.run, passes
a RunConfig, prints final_output, and includes notes about where to inspect
traces.
```

## Prompt 2

```text
Add a structured extractor example using a Pydantic output_type.

Use a calendar event extractor. Add tests for the Pydantic model without making
API calls.
```

## Prompt 3

```text
Add a function tool example with @function_tool.

The tool should return a small deterministic lookup result. The example should
print final_output and inspect new_items enough to see tool calls.
```

## Prompt 4

```text
Add a guardrail example that blocks requests outside a defined domain.

Include one allowed prompt and one blocked prompt. API-backed execution should
skip cleanly without OPENAI_API_KEY.
```

## Prompt 5

```text
Add a session memory example with two turns.

Show the difference between stateless execution and session-backed execution.
Add README instructions and run tests.
```

## Prompt 6

```text
Add a shared build_run_config helper that returns an OpenAI Agents SDK
RunConfig with workflow_name and trace_metadata.

Update every runnable example to call Runner.run with that RunConfig. Add a
local test that verifies the helper returns a real SDK RunConfig.
```
