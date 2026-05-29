from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any

from openai.types.responses import ResponseFunctionCallArgumentsDeltaEvent, ResponseTextDeltaEvent

from agents import Runner
from agents.exceptions import MaxTurnsExceeded
from agents.items import ItemHelpers
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


DEMO_PROMPT = """
Inspect the workspace, read repo/AGENTS.md, run the calculator tests from repo/,
identify the smallest fix, apply it, rerun tests, and summarize the change.
When the tests pass after your fix, stop using tools and provide the final
summary immediately.
"""
DEFAULT_MAX_TURNS = 20


async def close_export_delete(
    client: UnixLocalSandboxClient,
    sandbox: Any,
    *,
    export_dir: Path,
) -> Path | None:
    try:
        await sandbox.aclose()
    finally:
        try:
            exported = await export_workspace(sandbox, export_dir)
            print(f"\nExported final workspace to: {exported}")
        except Exception as exc:
            exported = None
            print(f"\nWorkspace export failed: {exc}")
        await client.delete(sandbox)
    return exported


async def run_demo(
    *,
    model: str,
    export_dir: Path,
    snapshot_dir: Path,
    max_turns: int = DEFAULT_MAX_TURNS,
) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to run the SandboxAgent demo.")

    client = UnixLocalSandboxClient()
    sandbox = await client.create(
        manifest=build_manifest(),
        options=UnixLocalSandboxClientOptions(),
        snapshot=LocalSnapshotSpec(base_path=snapshot_dir),
    )
    try:
        result = await Runner.run(
            build_sandbox_agent(model=model),
            DEMO_PROMPT,
            run_config=build_run_config_for_session(sandbox),
            max_turns=max_turns,
        )
        return str(result.final_output)
    except MaxTurnsExceeded:
        print(f"\n[lab-03] Max turns reached: max_turns={max_turns}.")
        print("[lab-03] Closing and exporting the workspace for inspection.")
        raise
    finally:
        await close_export_delete(client, sandbox, export_dir=export_dir)


def _tool_call_name(item: Any) -> str:
    raw_item = item.raw_item
    if isinstance(raw_item, dict):
        return str(raw_item.get("name") or raw_item.get("type") or "tool")
    return str(getattr(raw_item, "name", None) or getattr(raw_item, "type", None) or "tool")


def _format_tool_call_arguments(item: Any) -> str | None:
    raw_item = item.raw_item
    arguments = raw_item.get("arguments") if isinstance(raw_item, dict) else getattr(raw_item, "arguments", None)
    if not isinstance(arguments, str) or not arguments:
        return None
    try:
        return json.dumps(json.loads(arguments), indent=2, sort_keys=True)
    except json.JSONDecodeError:
        return arguments


def _shorten(value: object, *, limit: int = 500) -> str:
    text = str(value)
    return text if len(text) <= limit else f"{text[:limit]}..."


async def run_demo_streamed(
    *,
    model: str,
    export_dir: Path,
    snapshot_dir: Path,
    max_turns: int = DEFAULT_MAX_TURNS,
) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to run the SandboxAgent demo.")

    client = UnixLocalSandboxClient()
    sandbox = await client.create(
        manifest=build_manifest(),
        options=UnixLocalSandboxClientOptions(),
        snapshot=LocalSnapshotSpec(base_path=snapshot_dir),
    )

    print("[lab-03] Starting SandboxAgent streamed run.")
    print("[lab-03] Runtime: UnixLocal SandboxRunConfig")
    print("[lab-03] Workspace entry: repo/")
    print(f"[lab-03] Sandbox workspace root: {sandbox.state.manifest.root}")
    print(f"[lab-03] Local export target: {export_dir}")
    print("[lab-03] Prompt:")
    print(DEMO_PROMPT.strip())
    print()

    try:
        result = Runner.run_streamed(
            build_sandbox_agent(model=model),
            DEMO_PROMPT,
            run_config=build_run_config_for_session(sandbox),
            max_turns=max_turns,
        )

        text_open = False
        active_tool_call: str | None = None

        async for event in result.stream_events():
            if event.type == "agent_updated_stream_event":
                if text_open:
                    print()
                    text_open = False
                print(f"[agent] {event.new_agent.name}")
                continue

            if event.type == "raw_response_event":
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    if not text_open:
                        print("[model:text] ", end="", flush=True)
                        text_open = True
                    print(data.delta, end="", flush=True)
                    continue
                if text_open:
                    print()
                    text_open = False
                if isinstance(data, ResponseFunctionCallArgumentsDeltaEvent):
                    if active_tool_call is None:
                        active_tool_call = "tool"
                        print("[model:tool_args] ", end="", flush=True)
                    print(data.delta, end="", flush=True)
                    continue
                if getattr(data, "type", None) == "response.output_item.done" and active_tool_call:
                    print()
                    print(f"[model:tool_args] completed for {active_tool_call}")
                    active_tool_call = None
                continue

            if text_open:
                print()
                text_open = False

            if event.type != "run_item_stream_event":
                continue

            if event.item.type == "tool_call_item":
                tool_name = _tool_call_name(event.item)
                active_tool_call = tool_name
                print(f"[tool:call] {tool_name}")
                arguments = _format_tool_call_arguments(event.item)
                if arguments:
                    print(arguments)
            elif event.item.type == "tool_call_output_item":
                print(f"[tool:output] {_shorten(event.item.output)}")
            elif event.item.type == "message_output_item":
                message = ItemHelpers.text_message_output(event.item)
                print(f"[message:complete] {len(message)} characters")
            else:
                print(f"[event:{event.name}] item_type={event.item.type}")

        if text_open:
            print()

        print("\n[lab-03] Stream complete.")
        return str(result.final_output)
    except MaxTurnsExceeded:
        print(f"\n[lab-03] Max turns reached: max_turns={max_turns}.")
        print("[lab-03] Closing and exporting the workspace for inspection.")
        raise
    finally:
        exported = await close_export_delete(client, sandbox, export_dir=export_dir)
        if exported is not None:
            print(f"Inspect generated memory with: find {exported / 'memories'} -maxdepth 2 -type f")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run Lab 03 SandboxAgent demo.")
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Run without streaming progress events.",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_SANDBOX_MODEL", DEFAULT_SANDBOX_MODEL),
        help="Model for the SandboxAgent. Use a GPT-5 family model for custom tool support.",
    )
    parser.add_argument("--export-dir", default="artifacts/latest-workspace")
    parser.add_argument("--snapshot-dir", default="artifacts/snapshots")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=DEFAULT_MAX_TURNS,
        help="Maximum SDK turns before stopping and exporting the workspace.",
    )
    args = parser.parse_args(argv)

    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping API-backed SandboxAgent demo: OPENAI_API_KEY is not set.")
        print(
            "Set OPENAI_API_KEY, then rerun to create a UnixLocal sandbox and "
            "execute the Lab 03 debugging task."
        )
        return

    if args.no_stream:
        print(
            asyncio.run(
                run_demo(
                    model=args.model,
                    export_dir=Path(args.export_dir),
                    snapshot_dir=Path(args.snapshot_dir),
                    max_turns=args.max_turns,
                )
            )
        )
    else:
        final_output = asyncio.run(
            run_demo_streamed(
                model=args.model,
                export_dir=Path(args.export_dir),
                snapshot_dir=Path(args.snapshot_dir),
                max_turns=args.max_turns,
            )
        )
        print("\nFinal output:")
        print(final_output)


if __name__ == "__main__":
    main()
