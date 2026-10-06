# Mastering OpenAI Agents Labs

Use this repository to learn the OpenAI Agents SDK through Codex-built
reference solutions.

Codex is the construction partner. OpenAI Agents and SandboxAgents are the
subject matter.

The reference implementations are SDK-first: Lab 00 teaches Codex workflow,
Labs 01-02 and 04-05 use direct OpenAI Agents SDK `Agent` flows, and Lab 03 uses
direct SDK `SandboxAgent` with Unix-local `SandboxRunConfig`.

## Setup

Clone the repository with submodules so the SDK reference checkout is available
inside the repo-local skill:

```bash
git clone --recurse-submodules https://github.com/puria-izady/mastering-openai-agents.git
cd mastering-openai-agents
```

If you already cloned without submodules, initialize them once:

```bash
git submodule update --init --recursive
```

The submodule lives at:

```text
replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python
```

It points to the official
[`openai/openai-agents-python`](https://github.com/openai/openai-agents-python)
repository. The course pins a known SDK commit for reproducibility; update that
pin intentionally with `git submodule update --remote` and rerun the lab tests.

OpenAI Agents Python SDK repository:
<https://github.com/openai/openai-agents-python>

## Labs

| Lab | Title | Primary course purpose |
|---|---|---|
| 00 | Codex Workflow | Learn how to drive Codex before building agents |
| 01 | Agents SDK Sampler | Touch the core SDK primitives in small examples |
| 02 | Handoffs Patterns | Compare handoffs and agents-as-tools |
| 03 | SandboxAgent Sampler | Show workspace, shell, skills, memory, and resumption |
| 04 | SQL Analyzer Agent | First full business reference solution |
| 05 | Realtime Voice Agent | Compare Python voice pipelines with browser realtime sessions |

## Reproducible Prompts

Use `prompts-index.md` to find the reusable Codex prompt pack for each lab. Each
reference solution includes a `BUILD-LOG.md` recording the prompt IDs and local
verification.

## Testing References

Use `reference-test-guide.md` for the two test layers:

- offline contract tests, which do not call OpenAI;
- OpenAI API smoke tests, which require `OPENAI_API_KEY` and can be forced with
  `REQUIRE_OPENAI_API=1`.

Use `run-reference-guide.md` when you want to try the references interactively
without running pytest.

## Recommended Build Order

1. Use Labs 00-03 before Lab 04 so you see Codex workflow, Agents SDK
   primitives, orchestration, and SandboxAgent concepts first.
2. Use Lab 04 as the first full business reference solution.
3. Use Lab 05 after you understand normal `Agent` objects; the voice lab
   reuses those objects in Python voice and browser realtime architectures.

All labs have a local `reference-solution/` folder inside their lab
directory.
