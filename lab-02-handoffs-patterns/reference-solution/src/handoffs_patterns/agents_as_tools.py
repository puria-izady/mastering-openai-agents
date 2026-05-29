from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agents import Agent, Runner

from .agents_handoff import build_specialists
from .run_config import build_run_config


@dataclass(frozen=True)
class ManagerRunReport:
    final_output: str
    last_agent: str
    tool_outputs: list[str]


def collect_tool_outputs(result: Any) -> list[str]:
    outputs: list[str] = []
    for item in getattr(result, "new_items", []):
        if getattr(item, "type", None) != "tool_call_output_item":
            continue
        output = getattr(item, "output", None)
        if output is not None:
            outputs.append(str(output))
    return outputs


def build_manager(model: str = "gpt-5.5") -> Agent:
    billing, technical = build_specialists(model)
    return Agent(
        name="Support manager",
        instructions=(
            "You own the final reply. Call specialists as tools for their analysis, "
            "then synthesize one customer-ready answer."
        ),
        model=model,
        tools=[
            billing.as_tool(
                tool_name="ask_billing_specialist",
                tool_description="Get billing analysis for invoices, charges, refunds, or plans.",
            ),
            technical.as_tool(
                tool_name="ask_technical_specialist",
                tool_description="Get technical analysis for bugs, errors, exports, or integrations.",
            ),
        ],
    )


async def run_manager(prompt: str) -> str:
    result = await Runner.run(build_manager(), prompt, run_config=build_run_config())
    return str(result.final_output)


async def run_manager_report(prompt: str) -> ManagerRunReport:
    result = await Runner.run(build_manager(), prompt, run_config=build_run_config())
    return ManagerRunReport(
        final_output=str(result.final_output),
        last_agent=result.last_agent.name,
        tool_outputs=collect_tool_outputs(result),
    )
