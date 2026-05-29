# Prompt Pack: Lab 03

## Prompt 1

```text
Create a tiny buggy-calculator repo for a SandboxAgent lab.

Add AGENTS.md, one source file, and tests with one intentional failure.

Important SandboxAgent mounting requirement:
- The sandbox manifest must use relative destination paths only.
- Mount the calculator workspace under `repo`, not `/workspace`.
- Prefer synthetic SDK `Dir` and `File` manifest entries for the tiny lab repo
  instead of LocalDir, so UnixLocal works even when the course project lives in
  a macOS permission-restricted folder such as ~/Documents.
- Add a local smoke check that calls manifest.validated_entries().
```

## Prompt 2

```text
Create SandboxAgent lab instructions that ask the agent to inspect the workspace,
read AGENTS.md, run tests, and identify the failing behavior before editing.
```

## Prompt 3

```text
Add one skill called debug-failing-tests.

The skill should instruct the agent to reproduce the failure, locate the smallest
fix, run tests, and summarize the change.
```

## Prompt 4

```text
Add a memory exercise.

The agent should write a durable note about the repo convention, then a second
run should verify that the note is available.
```

## Prompt 5

```text
Add a UnixLocal SandboxRunConfig path.

Create a helper that returns RunConfig with SandboxRunConfig using
UnixLocalSandboxClient, UnixLocalSandboxClientOptions, and the lab manifest.
Manifest entry paths must be relative. Mount the calculator workspace as `repo`
using SDK `Dir` and `File` manifest entries so the demo is reliable in
permission-restricted local folders. Do not use an absolute `/workspace` entry.
Add a run_sandbox_demo.py entrypoint that calls Runner.run with that config. The
actual API-backed run should require OPENAI_API_KEY, while tests should validate
that the config can be constructed and that manifest.validated_entries() passes.
```

## Prompt 6

```text
Add streamed progress output for the SandboxAgent runner.

Use Runner.run_streamed and print:
- startup context, including UnixLocal runtime and workspace entry
- model text deltas
- tool calls and tool arguments
- tool outputs
- final output

Keep a --no-stream option for the non-streamed Runner.run path.
```
