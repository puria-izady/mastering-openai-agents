# OpenAI Agents Labs Replay Environment

This folder is the clean build space for replaying the lab prompts with Codex.
It intentionally contains reusable context, not finished reference solutions.

## Included Context

- `AGENTS.md`: course implementation rules for Codex.
- `.agents/skills/openai-agents-sdk/`: repo-local SDK Skill.
- `.agents/skills/openai-agents-sdk/openai-agents-python/`: submodule pointing
  to the official `openai/openai-agents-python` repository for examples, tests,
  and docs.
- `labs/*/prompt-pack.md`: prompt packs for Labs 01-05.

## SDK Submodule

Before replaying labs, make sure the SDK submodule has been initialized from
the repository root:

```bash
git submodule update --init --recursive
```

The course pins the submodule to a specific commit so examples and tests remain
reproducible. To refresh it intentionally:

```bash
git submodule update --remote replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python
```

After updating the SDK pin, rerun the local lab tests before sharing changes.

## How To Use

Start a new Codex task from this `replay-environment` folder and use one lab
prompt pack at a time.

Example for Lab 05:

```text
Use labs/lab-05-realtime-voice-agent/prompt-pack.md.
Follow the prompts in order.
Create the implementation in solutions/lab-05-realtime-voice-agent.
Do not inspect or copy from any reference-solution folder outside this replay
environment.
Use AGENTS.md, the openai-agents-sdk Skill, and the skill-local
openai-agents-python checkout as references.
```

## Replay Rules

- Build into `solutions/<lab-name>/`.
- Do not copy a finished `reference-solution/`.
- Use direct OpenAI Agents SDK objects.
- Keep SDK objects visible in code and tests.
- Make API-backed demos skip cleanly when `OPENAI_API_KEY` is absent.
- Record what prompt steps were used in the generated solution's `BUILD-LOG.md`.
