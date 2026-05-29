from __future__ import annotations

from agents import Agent, Runner, function_tool

from .run_config import build_run_config


LOOKUP = {
    "starter": "Best for teams trying their first internal copilot.",
    "pro": "Best for teams automating recurring workflows.",
    "enterprise": "Best for governed multi-agent deployments.",
}


@function_tool
def get_plan_note(plan: str) -> str:
    """Return a short note for a named product plan: starter, pro, or enterprise."""
    return LOOKUP.get(plan.lower(), "Unknown plan.")


def build_agent(model: str = "gpt-5.5") -> Agent:
    return Agent(
        name="Plan helper",
        instructions="Use get_plan_note when the user asks about a product plan.",
        model=model,
        tools=[get_plan_note],
    )


async def answer_plan_question(question: str) -> str:
    result = await Runner.run(build_agent(), question, run_config=build_run_config())
    return str(result.final_output)
