# Lab 01: OpenAI Agents SDK Capability Sampler

## Goal

Give yourself a fast, hands-on tour of the core OpenAI Agents SDK primitives.

## What You Build

An `agents-sdk-sampler` project with five small examples:

1. First agent
2. Structured extractor
3. Function tool
4. Guardrail
5. Session-backed memory

## OpenAI Agents Concepts

- `Agent`
- `Runner.run`
- `RunResult.final_output`
- `RunResult.new_items`
- Pydantic `output_type`
- `@function_tool`
- Input or output guardrail
- Session-backed conversation state
- Trace inspection

## Reference Solution Scope

Create one Python package with one runnable file per mini-lab:

```text
agents-sdk-sampler/
  src/agents_sampler/
    first_agent.py
    structured_extractor.py
    function_tool_demo.py
    guardrail_demo.py
    session_demo.py
  tests/
```

Tests should cover local schemas and helper functions. API-backed examples skip
without `OPENAI_API_KEY`.

## Checkpoint

You can identify which code belongs to the `Agent`, which code belongs to
tools, and what `Runner.run` returns.

