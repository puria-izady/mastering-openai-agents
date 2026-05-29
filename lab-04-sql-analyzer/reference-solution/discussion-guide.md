# Discussion Guide: SQL Analyzer Agent

## Why This Lab Matters

This is the first full business reference solution after the smaller OpenAI
Agents SDK capability samplers.

Use this lab to practice the complete Codex loop:

1. Ask Codex to scaffold.
2. Ask Codex to implement one capability.
3. Run tests.
4. Inspect the code.
5. Tighten the prompt.
6. Repeat.

## Main Concept

The agent is not useful because it can "write SQL." It is useful because it has
a controlled tool boundary:

- The model decides what to ask.
- The app validates whether the SQL is safe.
- The database runs only read-only queries.
- The final answer is structured and inspectable.

## OpenAI Agents Concepts

Pay attention to these points:

- `Agent` is the role, instructions, tools, model, and output contract.
- `Runner.run` owns the agent loop.
- `Runner.run(..., context=...)` passes application dependencies to tool code
  without putting them into model-visible conversation history.
- `ctx: RunContextWrapper[...]` is the way database-backed tools read that
  local context. The name `ctx` follows the official examples used in this lab.
- Function tools expose real application capabilities.
- Tool descriptions matter.
- Structured outputs reduce parsing glue.
- Traces are the first debugging surface.

## Codex Concepts

Notice how the Codex prompts are scoped:

- Prompt 1 does not ask for the agent yet.
- Prompt 2 asks for tools and tests only.
- Prompt 3 wires the API-backed agent after local behavior is stable.
- Prompt 4 hardens reliability.
- Prompt 5 converts the build into reusable lab material.

## Common Mistakes

- Asking Codex to build everything in one prompt.
- Letting SQL execution run before validation exists.
- Hiding the database path in environment mutation instead of SDK run context.
- Putting all safety rules only in the prompt.
- Writing tests that require exact model prose.
- Forgetting to inspect traces after the first successful run.

## Suggested Discussion Questions

- Which parts should be handled by the model, and which by deterministic code?
- Why do we validate SQL twice: before execution and inside SQLite?
- What would change if this connected to a production warehouse?
- Where would you add human approval?
- When would this need a specialist agent instead of one agent with tools?
