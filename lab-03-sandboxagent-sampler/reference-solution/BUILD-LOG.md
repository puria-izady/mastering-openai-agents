# Build Log: Lab 03

## Prompts Used

- Prompt 1: buggy calculator workspace.
  - Fixed mounting rule: use relative manifest destination `repo` and synthetic
    `Dir`/`File` entries, not absolute `/workspace` or host `LocalDir`.
- Prompt 2: SandboxAgent lab instructions.
- Prompt 3: `debug-failing-tests` skill.
- Prompt 4: memory exercise.
- Prompt 5: UnixLocal `SandboxRunConfig` path with relative synthetic manifest
  entries.
- Prompt 6: streamed SandboxAgent progress output.
- Prompt update: explicit sandbox memory lifecycle, workspace export, and short
  memory smoke runner.

## Verification

- `uv run --with pytest pytest -q`: 3 passed.
- Tests validate `SandboxAgent`, manifest, sandbox capabilities, and
  `RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(...)))`.

## Memory Lifecycle Update

Updated the reference solution to match the replay memory fix.

Implementation:

- Seeded `memories/` into the SDK manifest.
- Added explicit `Memory(...)` configuration with layout, read, and generation
  settings.
- Added a live-session `RunConfig` helper for
  `SandboxRunConfig(session=sandbox)`.
- Updated the streamed demo to create a live UnixLocal session, close it so
  memory can flush, export the workspace to `artifacts/latest-workspace`, and
  delete the temporary workspace after export.
- Added `run_memory_smoke.py` for a short two-run memory-only test.
- Added local tests for the manifest memory seed, memory configuration,
  live-session run config, and memory smoke runner.

Verification:

- `uv run --extra dev pytest` passed with 7 tests and 1 skipped
  API-backed test.
- `uv run python run_memory_smoke.py` skipped cleanly without `OPENAI_API_KEY`.

## Max-Turn And Cleanup Fix

Updated the reference solution after the streamed SandboxAgent demo reached
`MaxTurnsExceeded` after tests had already passed.

Implementation:

- Added an explicit instruction for the agent to stop using tools and provide
  the final summary once tests pass.
- Added `--max-turns`, defaulting to 20, and passed it to both
  `Runner.run_streamed(..., max_turns=...)` and the `--no-stream`
  `Runner.run(..., max_turns=...)` path.
- Moved close/export/delete into a shared cleanup path that runs in `finally`,
  including when `MaxTurnsExceeded` is raised.
- The cleanup closes the sandbox first so SDK memory generation can flush,
  exports `artifacts/latest-workspace`, then deletes the temporary UnixLocal
  workspace.
- Added local tests that assert the turn budget, cleanup path, and
  stop-after-tests instruction are present.

Verification:

- `uv run --extra dev pytest` passed with 9 tests and 1 skipped API-backed
  test.
- `uv run python -m sandbox_sampler.run_sandbox_demo --max-turns 30` skips
  cleanly without `OPENAI_API_KEY`.
- `uv run python -m sandbox_sampler.run_sandbox_demo --no-stream --max-turns 30`
  skips cleanly without `OPENAI_API_KEY`.


## 2026-10-05 — GPT-6 Luna default update

Updated text/sandbox agent defaults to `gpt-6-luna` and verified SDK model
contracts locally. Explicit model overrides remain available; dedicated
transcription, speech, and realtime models are unchanged.

Local pytest suite: **10 passed, 1 skipped**, using openai-agents 0.17.3.
API credentials were removed from the test environment. No live model calls
were made; this verifies configuration and local behavior, not live API access.
No-key demo check: skipped API execution successfully (exit 0).
