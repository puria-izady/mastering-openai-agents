from __future__ import annotations

import argparse
import asyncio
import os

from agents_sampler.first_agent import run_demo
from agents_sampler.function_tool_demo import answer_plan_question
from agents_sampler.guardrail_demo import answer_domain_question
from agents_sampler.session_demo import ask_with_session, build_session
from agents_sampler.structured_extractor import extract_event


def require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required to run this reference demo.")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run Lab 01 Agents SDK sampler demos.")
    parser.add_argument(
        "demo",
        choices=["first-agent", "structured", "tool", "guardrail", "session"],
        help="Demo to run.",
    )
    parser.add_argument("--prompt", default="", help="Override the default prompt.")
    args = parser.parse_args()

    require_api_key()

    if args.demo == "first-agent":
        prompt = args.prompt or "Explain what an OpenAI Agent is in two sentences."
        print(await run_demo(prompt))
    elif args.demo == "structured":
        prompt = args.prompt or "Schedule agent design review on 2026-05-15 with Ada and Grace."
        print((await extract_event(prompt)).model_dump_json(indent=2))
    elif args.demo == "tool":
        prompt = args.prompt or "Which product plan is best for workflow automation?"
        print(await answer_plan_question(prompt))
    elif args.demo == "guardrail":
        prompt = args.prompt or "How do handoffs work in the OpenAI Agents SDK?"
        print(await answer_domain_question(prompt))
    else:
        session = build_session("lab-01-demo")
        first = await ask_with_session("Remember that I prefer short answers.", session)
        second = await ask_with_session(args.prompt or "What answer style do I prefer?", session)
        print("First turn:")
        print(first)
        print("\nSecond turn:")
        print(second)


if __name__ == "__main__":
    asyncio.run(main())
