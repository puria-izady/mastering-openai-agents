# SandboxAgent Sampler

Reference solution for Lab 03.

This lab shows the SandboxAgent surfaces and configures the local Unix sandbox
runtime through `RunConfig(..., sandbox=SandboxRunConfig(...))`:

- workspace instructions with `AGENTS.md`
- filesystem and shell capabilities
- skill materialization
- memory layout
- UnixLocal `SandboxRunConfig`
- resumption worksheet
- memory smoke runner
- exported workspaces under `artifacts/`

The local tests instantiate the `SandboxAgent` and UnixLocal run config without
making API calls. The actual `Runner.run(...)` demo requires `OPENAI_API_KEY`.

## Run The Sandbox Demo

```bash
uv run python -m sandbox_sampler.run_sandbox_demo
```

The demo uses:

- `SandboxAgent`
- `RunConfig`
- `SandboxRunConfig`
- `UnixLocalSandboxClient`
- `UnixLocalSandboxClientOptions`

The demo creates an explicit live UnixLocal sandbox session, closes it so SDK
memory generation can flush, exports the final workspace to
`artifacts/latest-workspace`, then deletes the temporary UnixLocal workspace.
It defaults to `--max-turns 20`; if the turn limit is reached, the demo still
closes the sandbox, exports `artifacts/latest-workspace`, and deletes the
temporary UnixLocal workspace so the final files and memory can be inspected.

Increase the turn budget for slower runs:

```bash
OPENAI_API_KEY=... uv run python -m sandbox_sampler.run_sandbox_demo --max-turns 30
```

Run without streaming:

```bash
OPENAI_API_KEY=... uv run python -m sandbox_sampler.run_sandbox_demo --no-stream --max-turns 30
```

## Run The Memory Smoke Test

Use this when you only want to verify sandbox memory and skip the calculator
debugging task:

```bash
OPENAI_API_KEY=... uv run python run_memory_smoke.py
cat artifacts/memory-smoke-workspace/memories/MEMORY.md
cat artifacts/memory-smoke-workspace/memories/memory_summary.md
```

The first run writes a short note to `memories/MEMORY.md`. The second run
resumes the sandbox and reads the note back.
