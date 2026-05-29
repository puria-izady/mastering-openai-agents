from __future__ import annotations

import argparse
import asyncio
import os

from sql_analyzer.app import async_main


def require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required to run this reference demo.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Lab 04 SQL Analyzer Agent demo.")
    parser.add_argument(
        "--question",
        default="Which products generated the most revenue?",
        help="Business question to ask the SQL Analyzer Agent.",
    )
    args = parser.parse_args()
    require_api_key()
    raise SystemExit(asyncio.run(async_main([args.question])))
