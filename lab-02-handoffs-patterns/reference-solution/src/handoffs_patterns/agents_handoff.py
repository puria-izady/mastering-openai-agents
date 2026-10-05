from __future__ import annotations

from agents import Agent, Runner

from .run_config import build_run_config


def build_specialists(model: str = "gpt-6-luna") -> tuple[Agent, Agent]:
    billing = Agent(
        name="Billing specialist",
        handoff_description="Owns invoice, charge, refund, and plan-price questions.",
        instructions="Resolve billing questions. Ask for invoice IDs when needed.",
        model=model,
    )
    technical = Agent(
        name="Technical specialist",
        handoff_description="Owns bugs, errors, exports, integrations, and troubleshooting.",
        instructions="Resolve technical support questions with clear troubleshooting steps.",
        model=model,
    )
    return billing, technical


def build_triage_agent(model: str = "gpt-6-luna") -> Agent:
    billing, technical = build_specialists(model)
    return Agent(
        name="Support triage",
        instructions=(
            "Route each support request to the specialist who should own the reply. "
            "If the request spans billing and technical work, explain what information "
            "is needed and keep ownership."
        ),
        model=model,
        handoffs=[billing, technical],
    )


async def run_handoff(prompt: str) -> tuple[str, str]:
    result = await Runner.run(build_triage_agent(), prompt, run_config=build_run_config())
    return str(result.final_output), result.last_agent.name
