from __future__ import annotations

from pathlib import Path

from agents import RunConfig
from agents.sandbox import (
    Manifest,
    MemoryGenerateConfig,
    MemoryLayoutConfig,
    MemoryReadConfig,
    SandboxAgent,
)
from agents.sandbox.capabilities import Filesystem, Memory, Shell, Skills
from agents.sandbox.entries import Dir, File
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient, UnixLocalSandboxClientOptions
from agents.sandbox.session.base_sandbox_session import BaseSandboxSession
from agents.run_config import SandboxRunConfig


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SANDBOX_MODEL = "gpt-5-mini"
MEMORY_EXTRA_PROMPT = (
    "For this course lab, preserve durable repo conventions, the exact failing "
    "calculator behavior found, the smallest fix applied, and any verification "
    "commands that succeeded or were blocked."
)


def _file(path: Path) -> File:
    return File(content=path.read_bytes())


def _directory(path: Path) -> Dir:
    children = {
        child.name: _directory(child) if child.is_dir() else _file(child)
        for child in sorted(path.iterdir())
        if child.name not in {"__pycache__", ".pytest_cache"}
    }
    return Dir(children=children)


def build_manifest() -> Manifest:
    return Manifest(
        entries={
            "repo": _directory(ROOT / "buggy-calculator"),
            "memories": _directory(ROOT / "memories"),
        },
    )


def build_memory_capability(model: str = DEFAULT_SANDBOX_MODEL) -> Memory:
    return Memory(
        layout=MemoryLayoutConfig(memories_dir="memories", sessions_dir="sessions"),
        read=MemoryReadConfig(live_update=True),
        generate=MemoryGenerateConfig(
            phase_one_model=model,
            phase_two_model=model,
            extra_prompt=MEMORY_EXTRA_PROMPT,
        ),
    )


def build_sandbox_agent(model: str = DEFAULT_SANDBOX_MODEL) -> SandboxAgent:
    return SandboxAgent(
        name="Sandbox calculator fixer",
        instructions=(
            "Inspect the workspace, read repo/AGENTS.md, run tests from repo/, "
            "use the debug-failing-tests skill, and update memory with durable "
            "lessons. Treat paths as relative to the sandbox workspace root. "
            "When tests pass after the fix, stop using tools and provide the "
            "final summary immediately."
        ),
        model=model,
        default_manifest=build_manifest(),
        capabilities=[
            Filesystem(),
            Shell(),
            Skills(from_=_directory(ROOT / "skills")),
            build_memory_capability(model=model),
        ],
    )


def build_unix_local_sandbox_run_config() -> RunConfig:
    """Build a RunConfig that runs the SandboxAgent through UnixLocal."""
    return RunConfig(
        workflow_name="lab-03-sandboxagent-unix-local",
        sandbox=SandboxRunConfig(
            client=UnixLocalSandboxClient(),
            options=UnixLocalSandboxClientOptions(),
            manifest=build_manifest(),
        ),
    )


def build_run_config_for_session(session: BaseSandboxSession) -> RunConfig:
    return RunConfig(
        workflow_name="lab-03-sandboxagent-unix-local-live-session",
        trace_metadata={
            "course": "mastering-openai-agents",
            "lab": "lab-03",
            "workspace_entry": "repo",
            "memory_dir": "memories",
        },
        sandbox=SandboxRunConfig(session=session),
    )
