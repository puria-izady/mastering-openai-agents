from __future__ import annotations

from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, input_guardrail

from .models import DomainCheck
from .run_config import build_run_config


def classify_domain(text: str) -> DomainCheck:
    allowed_terms = {"agent", "agents", "tool", "tools", "handoff", "guardrail", "session"}
    lowered = text.lower()
    allowed = any(term in lowered for term in allowed_terms)
    return DomainCheck(
        allowed=allowed,
        reason="OpenAI Agents domain question." if allowed else "Outside the lab domain.",
    )


@input_guardrail
async def agents_domain_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list,
) -> GuardrailFunctionOutput:
    text = input if isinstance(input, str) else " ".join(str(item) for item in input)
    check = classify_domain(text)
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=not check.allowed)


def build_agent(model: str = "gpt-5.5") -> Agent:
    return Agent(
        name="Agents domain tutor",
        instructions="Answer only questions about the OpenAI Agents SDK.",
        model=model,
        input_guardrails=[agents_domain_guardrail],
    )


async def answer_domain_question(question: str) -> str:
    result = await Runner.run(build_agent(), question, run_config=build_run_config())
    return str(result.final_output)
