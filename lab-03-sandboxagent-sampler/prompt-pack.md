# Prompt Pack: Lab 03


Default all SDK Agent/SandboxAgent model settings to `gpt-6-luna`. Keep modality-specific transcription, speech, and realtime audio model IDs unchanged.

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

The instructions should explain that the calculator repository is mounted at
`repo` and the seeded `memories/` directory is at the sandbox workspace root,
alongside `repo`. After the smallest fix is made and tests pass, have the agent
write a durable note about the repository convention and exact verification
command to `memories/MEMORY.md`, keep `memories/memory_summary.md` consistent,
and reread both files to verify the note. Explicitly tell it not to use
`../memories` from inside `repo`, since that path escapes the sandbox root.
After the memory note is written and verified, it should stop using tools and
immediately provide the final summary.
```

## Prompt 3

```text
Add one skill called debug-failing-tests.

The skill should instruct the agent to reproduce the failure, locate the smallest
fix, run tests, and summarize the change.
```

## Prompt 4

```text
Implement persistent file-based memory across two SandboxAgent runs in this lab.

Keep this as course material, not a required local two-run API test. Seed
`memories/MEMORY.md` and `memories/memory_summary.md` locally and in the
manifest (`Dir`/`File` entries under relative `memories/`). Since `repo` and
`memories/` are siblings at the sandbox root, instruct the agent to use
`memories/...` directly, never `../memories` from inside `repo`.

Configure `Memory` explicitly with `MemoryLayoutConfig(memories_dir="memories",
sessions_dir="sessions")`, `MemoryReadConfig(live_update=True)`, and
`MemoryGenerateConfig` using the runner model plus brief guidance to preserve
repo conventions, minimal fixes, and verification commands. Keep
`Filesystem()`, `Shell()`, `Skills(...)`, and `Memory(...)` explicit. Add local
checks for the seeded files and Memory capability.

Add a short worksheet: run one writes and rereads the repo convention and test
command in both files; run two reads them and reports the saved note. Explain
that generated memory is under `<sandbox-root>/memories/`, show `find`/`cat`
inspection commands, and note that temporary UnixLocal workspaces may vanish.
Runnable demos should export the workspace to `artifacts/` before cleanup so
generated memory remains inspectable.
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

Use `gpt-6-luna` as the default model, because the
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
Create run_memory_demo.py: one command performs two SandboxAgent runs and
verifies that SDK memory generation produces two distinct raw memories.

Use the lab agent with Memory reads and generation enabled. Create one
LocalSnapshot with a unique ID per invocation under artifacts/memory-snapshots;
pass the same snapshot object to both UnixLocalSandboxClient.create calls.
Use the lab manifest with relative paths and
RunConfig(sandbox=SandboxRunConfig(session=sandbox)), with a distinct group_id
for each run and fresh conversation history.

1. Start the first sandbox. Ask the agent to read repo/AGENTS.md and inspect
   the calculator source, then report a concrete repo convention and its source.
2. Close it to flush SDK memory generation and save the snapshot. Verify one
   raw_memories/*.md file exists; retain its name and contents.
3. Create and start a second sandbox from the same snapshot. Verify the first
   memory survived. Ask the agent to read that memory, inspect and run the
   calculator tests, and report how the convention applies and what tests
   revealed. Do not repair the calculator in this memory-only demo.
4. Close the second sandbox, then export to artifacts/memory-demo-workspace.
   Verify two distinct raw_memories/*.md files, the unchanged first raw memory,
   and matching rollout_summaries/*.md files. Print their paths and both final
   outputs. Fail clearly if generation or verification fails.

Use `await sandbox.aclose()` to close a sandbox session explicitly. The SDK
session exposes `aclose()`. Call `await client.delete(sandbox)`
after `aclose()` when the temporary UnixLocal workspace should be removed.
```
