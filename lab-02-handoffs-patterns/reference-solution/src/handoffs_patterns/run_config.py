from __future__ import annotations

from agents import RunConfig


def build_run_config() -> RunConfig:
    return RunConfig(
        workflow_name="lab-02-handoffs-patterns",
        trace_metadata={"lab": "02", "course": "mastering-openai-agents"},
    )
