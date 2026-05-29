from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from agents import Runner
from agents.sandbox import LocalSnapshotSpec
from agents.sandbox.sandboxes.unix_local import (
    UnixLocalSandboxClient,
    UnixLocalSandboxClientOptions,
)

from .build_agent import (
    DEFAULT_SANDBOX_MODEL,
    build_manifest,
    build_run_config_for_session,
    build_sandbox_agent,
)
from .workspace_export import export_workspace

WRITE_PROMPT = """Write this exact durable note into memories/MEMORY.md:

Smoke test memory note: the calculator repo convention is available.

Then update memories/memory_summary.md so it mentions "Smoke test memory note".
Do not inspect or edit repo files."""

READ_PROMPT = """Read memories/MEMORY.md and memories/memory_summary.md. Reply
with exactly one sentence confirming whether the smoke test memory note is
available."""


async def main_async() -> None:
    parser = argparse.ArgumentParser(description="Run the shortest Lab 03 memory smoke test.")
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_SANDBOX_MODEL", DEFAULT_SANDBOX_MODEL),
    )
    parser.add_argument("--export-dir", default="artifacts/memory-smoke-workspace")
    parser.add_argument("--snapshot-dir", default="artifacts/memory-smoke-snapshots")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("Skipping API-backed memory smoke test: OPENAI_API_KEY is not set.")
        return

    agent = build_sandbox_agent(model=args.model)
    client = UnixLocalSandboxClient()
    sandbox = await client.create(
        manifest=build_manifest(),
        options=UnixLocalSandboxClientOptions(),
        snapshot=LocalSnapshotSpec(base_path=Path(args.snapshot_dir)),
    )

    try:
        async with sandbox:
            first = await Runner.run(
                agent,
                WRITE_PROMPT,
                run_config=build_run_config_for_session(sandbox),
                max_turns=6,
            )
            print("[write]")
            print(first.final_output)

        frozen_state = client.deserialize_session_state(
            client.serialize_session_state(sandbox.state)
        )
        resumed = await client.resume(frozen_state)
        try:
            async with resumed:
                second = await Runner.run(
                    agent,
                    READ_PROMPT,
                    run_config=build_run_config_for_session(resumed),
                    max_turns=6,
                )
                print("\n[read]")
                print(second.final_output)

            exported = await export_workspace(resumed, Path(args.export_dir))
            print(f"\nExported workspace: {exported}")
            print(f"Inspect: cat {exported / 'memories' / 'MEMORY.md'}")
        finally:
            await client.delete(resumed)
    finally:
        await client.delete(sandbox)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
