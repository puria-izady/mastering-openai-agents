from __future__ import annotations

import argparse
import asyncio
import os

from handoffs_patterns.agents_as_tools import run_manager_report
from handoffs_patterns.agents_handoff import run_handoff


def require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required to run this reference demo.")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run Lab 02 orchestration demos.")
    parser.add_argument("mode", choices=["handoff", "tools"], help="Orchestration pattern.")
    parser.add_argument(
        "--prompt",
        default="My invoice is higher this month and the dashboard export is broken.",
    )
    args = parser.parse_args()

    require_api_key()

    if args.mode == "handoff":
        output, last_agent = await run_handoff(args.prompt)
        print("Final output:")
        print(output)
        print(f"\nLast agent: {last_agent}")
    else:
        report = await run_manager_report(args.prompt)
        print("Final output:")
        print(report.final_output)
        print(f"\nLast agent: {report.last_agent}")
        print("\nTool outputs:")
        if report.tool_outputs:
            for index, output in enumerate(report.tool_outputs, start=1):
                print(f"\n[{index}]")
                print(output)
        else:
            print("(no tool outputs captured)")


if __name__ == "__main__":
    asyncio.run(main())
