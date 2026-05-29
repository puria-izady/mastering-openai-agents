from __future__ import annotations

from agents import RunConfig


def build_run_config() -> RunConfig:
    return RunConfig(
        workflow_name="lab-01-agents-sdk-sampler",
        trace_metadata={"lab": "01", "course": "mastering-openai-agents"},
    )
