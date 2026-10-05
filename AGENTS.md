# Mastering OpenAI Agents Labs Guide

This repository contains Codex-built course labs for the OpenAI Agents SDK. Create course content as Markdown (`*.md`) and not as PPTX.

## Repository Layout

Expected structure:

```text
lab-00-codex-workflow/
lab-01-agents-sdk-sampler/
lab-02-handoffs-patterns/
lab-03-sandboxagent-sampler/
lab-04-sql-analyzer/
lab-05-realtime-voice-agent/
replay-environment/
  .agents/
    skills/
      openai-agents-sdk/
        SKILL.md
        references/
        openai-agents-python/  # Git submodule
```

When carving this folder out into a dedicated repository, include:

- `AGENTS.md`
- `lab-00-*` through `lab-05-*`
- `replay-environment/`
- repository-level guides such as `README.md`, `prompts-index.md`,
  `run-reference-guide.md`, and `reference-test-guide.md`

Do not include unrelated parent-course slide decks, generated slide assets, or
other folders from the original workspace.

Each lab folder should contain:

- `prompt-pack.md`: reproducible Codex build prompts.
- `lab-brief.md`: short lab status, goal, and concepts.
- `reference-solution/`: finished reference implementation, when the lab has
  been built.

Each `reference-solution/` should contain:

- `README.md`
- `BUILD-LOG.md`
- `run_reference.py` or equivalent runnable demo
- local tests
- Markdown reusable lab materials where relevant

## Course Implementation Rules

- Default text and sandbox agents, including sandbox memory generation, to
  `gpt-6-luna`. Preserve explicit model overrides and dedicated transcription,
  speech, and realtime audio model IDs.
- Use the OpenAI Agents SDK directly. Do not hide the SDK behind
  course-specific framework abstractions such as custom runner, workflow, or
  base-agent layers.
- Lab 00 is Codex workflow only.
- Labs 01-02 and 04-05 use SDK `Agent` objects.
- Lab 03 uses SDK `SandboxAgent`.
- Keep important SDK objects visible in the labs: `Agent`, `SandboxAgent`,
  `Runner`, `RunConfig`, `SandboxRunConfig`, tools, handoffs, guardrails,
  sessions, `RunState`, tracing, and tracing metadata.
- Small helpers such as `build_agent()`, `build_run_config()`, or
  `build_context()` are allowed when they return real SDK objects and keep the
  SDK surface visible.
- Deterministic/local code belongs in fixtures, function-tool implementations,
  eval helpers, and tests. It must not replace the SDK agent flow in SDK labs.
- API-backed demos should require `OPENAI_API_KEY`, but local tests must run
  without making model calls.

## Skill And SDK Reference

Use the repo-local `$openai-agents-sdk` Skill for SDK lab work:

`replay-environment/.agents/skills/openai-agents-sdk/SKILL.md`

The official SDK checkout should be available inside the Skill:

`replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python`

This checkout is a Git submodule pointing to the official
`openai/openai-agents-python` repository. Initialize it with
`git submodule update --init --recursive` after cloning.

Use that checkout for examples, tests, docs, and implementation patterns. Use
the OpenAI Docs MCP for current public guidance when changing SDK usage.

If the Skill-local `openai-agents-python` checkout is missing, restore it before
reworking SDK labs or replaying prompt packs.

## Lab Prompt Packs

Each lab prompt pack is a reproducible Codex build script.

When creating or reworking a reference solution:

- follow prompts in order,
- keep prompts in Markdown,
- record prompt IDs and verification in `reference-solution/BUILD-LOG.md`,
- update the lab-level `prompt-pack.md` so replay does not depend on reading
  inside `reference-solution/`,
- make API-backed demos skip cleanly when `OPENAI_API_KEY` is absent,
- run local tests for deterministic behavior and SDK object contracts.

Lab-level `prompt-pack.md` files must be complete enough for replay. They
should not only point to `reference-solution/prompt-pack.md`.

## Replay Environment

The replay environment is for rebuilding labs from scratch with Codex.

`replay-environment/` should include:

- `AGENTS.md`
- `.agents/skills/openai-agents-sdk/`
- `.agents/skills/openai-agents-sdk/openai-agents-python/`
- `labs/<lab-name>/prompt-pack.md`
- `solutions/`

Replay rules:

- Build into `replay-environment/solutions/<lab-name>/`.
- Do not copy a finished `reference-solution/`.
- Do not inspect `reference-solution/` while replaying a lab prompt unless the
  user explicitly asks for a comparison.
- Use `AGENTS.md`, the SDK Skill, and the skill-local `openai-agents-python`
  checkout as the reference material.
- Record replay prompt steps and verification in the generated solution's
  `BUILD-LOG.md`.

Recommended replay prompt:

```text
Use labs/<lab-name>/prompt-pack.md.
Follow the prompts in order.
Create the implementation in solutions/<lab-name>.
Do not inspect or copy from any reference-solution folder.
Use AGENTS.md, the openai-agents-sdk Skill, and the skill-local
openai-agents-python checkout as references.
```

## Lab-Specific Rules

Lab 01:

- Use direct SDK `Agent`, `Runner.run`, `RunConfig`, structured outputs,
  function tools, guardrails, and sessions.
- Runnable demos should print `final_output` and show useful run artifacts.

Lab 02:

- Include both handoffs and agents-as-tools variants.
- Handoff examples must use real SDK `handoffs=[...]`.
- Agents-as-tools examples must use `specialist.as_tool(...)`.
- Runners should print final output, `last_agent`, and captured tool outputs
  where relevant.

Lab 03:

- Use SDK `SandboxAgent`.
- Use Unix-local sandbox configuration unless the lab explicitly says otherwise:
  `RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(...)))`.
- Manifest destination paths must be relative. Do not mount to absolute
  `/workspace`.
- Prefer synthetic SDK `Dir` and `File` manifest entries for tiny lab repos
  so UnixLocal works in macOS permission-restricted folders.
- Provide streamed progress output with `Runner.run_streamed` for the demo.

Lab 04:

- Use `Agent[SqlAnalyzerContext]` and pass the database dependency through
  `Runner.run(..., context=...)`.
- Database-backed tools should receive
  `ctx: RunContextWrapper[SqlAnalyzerContext]` and read from `ctx.context`.
- Do not rely on environment mutation or module-level global database state for
  tool execution.
- Keep SQL execution behind deterministic read-only function tools.
- Keep `AnalysisAnswer` strict JSON schema compatible. Do not use
  `dict[str, Any]` fields in the final output model.
- Instruct the agent to generate SQL without semicolons and to repair a
  semicolon-only validation failure by validating again before execution.

Lab 05:

- Keep the reusable text agent as a real SDK `Agent`.
- Use the Python SDK `VoicePipeline` path for chained speech-to-text, agent
  reasoning, and text-to-speech demos.
- Keep the browser realtime implementation separate: use TypeScript
  `RealtimeAgent` and `RealtimeSession` over WebRTC with a trusted token server.
- Never expose a standard `OPENAI_API_KEY` to browser code; the browser should
  receive only an ephemeral realtime client secret.
- Local tests must not require audio hardware or call the OpenAI API.

## Verification Expectations

For each reference solution:

- Run the lab's local tests.
- Run the lab's demo runner when possible.
- Run eval commands when present.
- API-backed tests should skip cleanly when `OPENAI_API_KEY` is absent.
- Add or update tests for SDK object contracts when changing SDK usage, for
  example `RunConfig`, `AgentOutputSchema`, `RunContextWrapper`, handoffs,
  tool schemas, or sandbox manifest validation.
