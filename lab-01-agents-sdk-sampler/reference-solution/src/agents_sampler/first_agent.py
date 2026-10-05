from __future__ import annotations

from agents import Agent, Runner

from .run_config import build_run_config


def build_agent(model: str = "gpt-6-luna") -> Agent:
    return Agent(
        name="Concise tutor",
        instructions="Answer clearly in three sentences or fewer.",
        model=model,
    )


async def run_demo(prompt: str) -> str:
    result = await Runner.run(build_agent(), prompt, run_config=build_run_config())
    return str(result.final_output)
