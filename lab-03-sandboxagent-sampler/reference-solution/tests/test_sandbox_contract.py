from agents import RunConfig
from agents.sandbox import MemoryGenerateConfig, MemoryLayoutConfig, MemoryReadConfig, SandboxAgent
from agents.sandbox.capabilities import Memory
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient, UnixLocalSandboxClientOptions

from sandbox_sampler.build_agent import (
    DEFAULT_SANDBOX_MODEL,
    build_manifest,
    build_memory_capability,
    build_run_config_for_session,
    build_sandbox_agent,
    build_unix_local_sandbox_run_config,
)


def test_manifest_mounts_buggy_calculator() -> None:
    manifest = build_manifest()
    assert "repo" in {str(path) for path in manifest.entries}
    assert manifest.validated_entries()


def test_manifest_seeds_memory_files() -> None:
    entries = build_manifest().validated_entries()
    assert "memories" in entries
    memories = entries["memories"]
    assert "MEMORY.md" in memories.children
    assert "memory_summary.md" in memories.children


def test_sandbox_agent_has_expected_capabilities() -> None:
    agent = build_sandbox_agent()
    assert isinstance(agent, SandboxAgent)
    assert agent.model == DEFAULT_SANDBOX_MODEL
    assert "stop using tools" in agent.instructions
    capability_names = {capability.type for capability in agent.capabilities}
    assert {"filesystem", "shell", "skills", "memory"}.issubset(capability_names)


def test_unix_local_run_config_is_configured() -> None:
    run_config = build_unix_local_sandbox_run_config()
    assert run_config.workflow_name == "lab-03-sandboxagent-unix-local"
    assert run_config.sandbox is not None
    assert isinstance(run_config.sandbox.client, UnixLocalSandboxClient)
    assert isinstance(run_config.sandbox.options, UnixLocalSandboxClientOptions)
    assert run_config.sandbox.manifest is not None


def test_memory_capability_has_explicit_layout_and_generation_models() -> None:
    memory = build_memory_capability(model="gpt-5-mini")

    assert isinstance(memory, Memory)
    assert isinstance(memory.layout, MemoryLayoutConfig)
    assert memory.layout.memories_dir == "memories"
    assert memory.layout.sessions_dir == "sessions"
    assert isinstance(memory.read, MemoryReadConfig)
    assert memory.read.live_update is True
    assert isinstance(memory.generate, MemoryGenerateConfig)
    assert memory.generate.phase_one_model == "gpt-5-mini"
    assert memory.generate.phase_two_model == "gpt-5-mini"


def test_build_run_config_for_session_returns_sdk_run_config() -> None:
    class _Session:
        pass

    run_config = build_run_config_for_session(_Session())  # type: ignore[arg-type]

    assert isinstance(run_config, RunConfig)
    assert run_config.sandbox is not None
    assert run_config.sandbox.session is not None
    assert run_config.trace_metadata["memory_dir"] == "memories"


def test_memory_smoke_runner_is_memory_only() -> None:
    from pathlib import Path

    demo = Path("src/sandbox_sampler/run_memory_smoke.py").read_text(encoding="utf-8")

    assert "WRITE_PROMPT" in demo
    assert "READ_PROMPT" in demo
    assert "Smoke test memory note" in demo
    assert "client.resume" in demo
    assert "export_workspace" in demo
    assert "Do not inspect or edit repo files." in demo


def test_sandbox_demo_has_turn_budget_and_failure_cleanup() -> None:
    from pathlib import Path

    demo = Path("src/sandbox_sampler/run_sandbox_demo.py").read_text(encoding="utf-8")

    assert "DEFAULT_MAX_TURNS = 20" in demo
    assert "--max-turns" in demo
    assert "max_turns=args.max_turns" in demo
    assert "MaxTurnsExceeded" in demo
    assert "close_export_delete" in demo
    assert "await sandbox.aclose()" in demo
    assert "await export_workspace(sandbox, export_dir)" in demo
    assert "await client.delete(sandbox)" in demo
    assert "stop using tools" in demo


def test_sandbox_demo_skips_cleanly_without_api_key(monkeypatch, capsys) -> None:
    from sandbox_sampler.run_sandbox_demo import main

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    main([])

    output = capsys.readouterr().out
    assert "Skipping API-backed SandboxAgent demo" in output
    assert "OPENAI_API_KEY is not set" in output
