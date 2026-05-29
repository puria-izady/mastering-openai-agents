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

The instructions must also tell the agent that once the fix is made and tests
pass, it should stop using tools and immediately provide the final summary. This
prevents the demo from continuing to call tools after the debugging task is
complete.
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

Keep this as course material, not a required local two-run API test. Add a
Markdown resumption worksheet and seeded memory files such as
`memories/MEMORY.md` and `memories/memory_summary.md`. Local tests should verify
that the files exist and that the SandboxAgent has the `Memory` capability.

Important: seed those same memory files into the SDK sandbox manifest under a
relative `memories` entry using SDK `Dir` and `File` entries. The local
`memories/` folder is the stable course artifact, but API-backed runs should
start with `memories/MEMORY.md` and `memories/memory_summary.md` already present
inside the active sandbox workspace.

Configure memory explicitly instead of using a bare `Memory()`:
- use `MemoryLayoutConfig(memories_dir="memories", sessions_dir="sessions")`
- use `MemoryReadConfig(live_update=True)`
- use `MemoryGenerateConfig(...)` with the same model used for the lab runner
  and a short extra prompt that preserves repo conventions, smallest fixes, and
  verification commands

Keep `Filesystem()`, `Shell()`, `Skills(...)`, and `Memory(...)` as explicit
capabilities. Memory reads need shell access, and live updates need filesystem
access.

The worksheet must include concrete inspection guidance for generated memory:
- explain that generated sandbox memory normally lives under `memories/` in the
  active sandbox workspace
- tell you to inspect `memories/MEMORY.md` and
  `memories/memory_summary.md`
- include example commands using the sandbox workspace path printed or observed
  during the run, for example `find <sandbox-root>/memories -maxdepth 2 -type f`
  and `cat <sandbox-root>/memories/MEMORY.md`
- mention that temporary UnixLocal sandbox workspaces may be deleted after
  cleanup, so the stable seeded course artifact is the local `memories/` folder
- mention that runnable demos should export the final sandbox workspace into
  `artifacts/` before deleting the temporary UnixLocal workspace, so generated
  memories remain inspectable after the process exits
```

## Prompt 5

```text
Add a UnixLocal SandboxRunConfig path.

Create a helper that returns RunConfig with SandboxRunConfig using
UnixLocalSandboxClient, UnixLocalSandboxClientOptions, and the lab manifest.
Create the SandboxAgent with the exact sandbox capabilities needed by this lab:
`Filesystem()`, `Shell()`, `Skills(...)`, and `Memory()` from
`agents.sandbox.capabilities`.
Do not rely on implicit/default capabilities for this lab; the agent must be
able to inspect/edit files, run shell commands, load the `debug-failing-tests`
skill, and use memory.
Manifest entry paths must be relative. Mount the calculator workspace as `repo`
using SDK `Dir` and `File` manifest entries so the demo is reliable in
permission-restricted local folders. Do not use an absolute `/workspace` entry.
Add a run_sandbox_demo.py entrypoint that calls Runner.run with that config. The
actual API-backed run should require OPENAI_API_KEY, while tests should validate
that the config can be constructed, that manifest.validated_entries() passes,
and that the SandboxAgent exposes `Filesystem`, `Shell`, `Skills`, and `Memory`
capabilities.

Also add a live-session config helper that returns `RunConfig` with
`SandboxRunConfig(session=sandbox)`. Use it in runnable demos where the course
code needs to control the UnixLocal lifecycle explicitly.
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

Use a GPT-5 family model by default, for example `gpt-5-mini`, because the
`Filesystem()` capability exposes `apply_patch` as a Responses custom tool.
Add a `--model` CLI option and `OPENAI_SANDBOX_MODEL` override.
Add a `--max-turns` CLI option with a default of at least 20, because the
debugging loop needs enough room to inspect, reproduce, edit, retest, and
summarize. Pass this value to both `Runner.run_streamed(..., max_turns=...)`
and the `--no-stream` `Runner.run(..., max_turns=...)` path.

The streamed demo should:
- create an explicit live UnixLocal sandbox session with the lab manifest
- use `LocalSnapshotSpec` so the workspace can be snapshotted/resumed
- pass `RunConfig(sandbox=SandboxRunConfig(session=sandbox))`
- close the sandbox session so SDK memory generation can flush
- export the final workspace to `artifacts/latest-workspace`
- delete the temporary UnixLocal workspace only after export

Important cleanup and failure behavior:
- Put close/export/delete cleanup in a `finally` path so it runs even if the
  run raises `MaxTurnsExceeded` or another exception after the agent has edited
  files.
- Close the sandbox session before exporting so SDK memory generation can flush.
- Export `artifacts/latest-workspace` before deleting the temporary UnixLocal
  workspace.
- If `MaxTurnsExceeded` occurs, print a short message explaining that the turn
  limit was reached and that the workspace is still being exported for
  inspection.
- Add local tests that verify the runner exposes `--max-turns`, uses
  `LocalSnapshotSpec`, uses the live-session `RunConfig`, exports the workspace
  in the cleanup path, and handles `MaxTurnsExceeded` without skipping cleanup.
```

## Prompt 7

```text
Add a short memory-only smoke runner.

Create `run_memory_smoke.py` that skips the calculator debugging task. It should
only verify sandbox memory:

1. Create a live UnixLocal sandbox session with the lab manifest and
   `LocalSnapshotSpec`.
2. Run the SandboxAgent once with a prompt that writes a small durable note to
   `memories/MEMORY.md` and updates `memories/memory_summary.md`.
3. Close the session so SDK memory generation can flush.
4. Serialize and resume the sandbox session state with the same
   `UnixLocalSandboxClient`.
5. Run the SandboxAgent a second time with a prompt that reads
   `memories/MEMORY.md` and `memories/memory_summary.md` and confirms the note is
   available.
6. Export the final resumed workspace to `artifacts/memory-smoke-workspace`
   before deleting the temporary UnixLocal workspace.

The script should require `OPENAI_API_KEY` for API-backed execution and skip
cleanly without it.

Add README instructions:

```bash
OPENAI_API_KEY=... uv run --extra dev python run_memory_smoke.py
cat artifacts/memory-smoke-workspace/memories/MEMORY.md
cat artifacts/memory-smoke-workspace/memories/memory_summary.md
```

Add local tests that verify the smoke runner exists, uses `client.resume`, uses
workspace export, references `memories/MEMORY.md`, and does not ask the agent to
debug the calculator repo.
```
