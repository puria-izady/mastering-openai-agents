from __future__ import annotations

try:
    from agents import RunConfig
except ImportError as exc:  # pragma: no cover - exercised only before dependency install.
    raise RuntimeError(
        "openai-agents is required to build the SQL Analyzer RunConfig. "
        "Install with: pip install -e '.[dev]'"
    ) from exc


def build_run_config() -> RunConfig:
    return RunConfig(
        workflow_name="lab-04-sql-analyzer",
        trace_metadata={"lab": "04", "course": "mastering-openai-agents"},
    )
