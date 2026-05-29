# Mastering OpenAI Agents Replay Guide

This folder is for rebuilding lab solutions from prompt packs with Codex. It is
not a reference-solution folder.

Create course content as Markdown (`*.md`) and not as PPTX.

## Replay Layout

Expected structure:

```text
AGENTS.md
README.md
.agents/
  skills/
    openai-agents-sdk/
      SKILL.md
      references/
      openai-agents-python/
labs/
  lab-01-agents-sdk-sampler/prompt-pack.md
  lab-02-handoffs-patterns/prompt-pack.md
  lab-03-sandboxagent-sampler/prompt-pack.md
  lab-04-sql-analyzer/prompt-pack.md
solutions/
```

Build generated work into:

`solutions/<lab-name>/`

## SDK Rules

- Use the OpenAI Agents SDK directly.
- Do not create course-specific runner, workflow, or base-agent abstraction
  layers.
- Keep SDK objects visible in code and tests: `Agent`, `SandboxAgent`,
  `Runner`, `RunConfig`, `SandboxRunConfig`, tools, handoffs, guardrails,
  sessions, `RunState`, and tracing metadata.
- Small helpers such as `build_agent()`, `build_run_config()`, and
  `build_context()` are allowed only when they return real SDK objects.
- Deterministic code belongs in fixtures, function-tool implementations, eval
  helpers, and tests. It must not replace the SDK agent flow.
- API-backed demos should require `OPENAI_API_KEY`, but local tests must run
  without making model calls.

## Skill Usage

Use the repo-local `$openai-agents-sdk` Skill:

`.agents/skills/openai-agents-sdk/SKILL.md`

Use the official SDK checkout nested inside the Skill for examples, tests, and
implementation patterns:

`.agents/skills/openai-agents-sdk/openai-agents-python`

Use the OpenAI Docs MCP for current public guidance when changing SDK usage.

## Replay Rules

- Follow the selected lab prompt pack in order.
- Do not inspect or copy a finished `reference-solution/` from outside this
  replay environment.
- Create or update a `BUILD-LOG.md` inside the generated solution.
- Record prompt steps and verification results in that build log.
- Run local tests after each substantial step.
- If a model/API-backed demo cannot run because `OPENAI_API_KEY` is absent,
  make it skip cleanly and verify deterministic tests still pass.

Recommended starting prompt:

```text
Use labs/<lab-name>/prompt-pack.md.
Follow the prompts in order.
Create the implementation in solutions/<lab-name>.
Do not inspect or copy from any reference-solution folder.
Use AGENTS.md, the openai-agents-sdk Skill, and the skill-local
openai-agents-python checkout as references.
```

## Lab-Specific Replay Notes

Lab 01:

- Use direct SDK `Agent`, `Runner.run`, `RunConfig`, structured outputs,
  function tools, guardrails, and sessions.

Lab 02:

- Include both real SDK handoffs and `agent.as_tool(...)` variants.
- Print final output, `last_agent`, and captured specialist tool outputs where
  relevant.

Lab 03:

- Use SDK `SandboxAgent`.
- Use Unix-local sandbox configuration:
  `RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(...)))`.
- Manifest paths must be relative. Do not use absolute `/workspace`.
- Prefer synthetic SDK `Dir` and `File` manifest entries for tiny lab repos.
- Stream demo progress with `Runner.run_streamed`.

Lab 04:

- Use `Agent[SqlAnalyzerContext]`.
- Pass the database dependency with `Runner.run(..., context=...)`.
- Database-backed tools should receive
  `ctx: RunContextWrapper[SqlAnalyzerContext]`.
- Keep the final `AnalysisAnswer` strict JSON schema compatible.
- Do not use `dict[str, Any]` fields in the final output model.
- Generate SQL without semicolons and repair semicolon-only validation failures
  by validating again before execution.

