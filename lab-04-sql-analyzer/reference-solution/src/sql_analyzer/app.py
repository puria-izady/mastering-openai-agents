from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv

from .agent import build_agent
from .context import build_context
from .run_config import build_run_config
from .schemas import AnalysisAnswer

try:
    from agents import Runner, trace
except ImportError as exc:  # pragma: no cover - exercised only before dependency install.
    raise RuntimeError(
        "openai-agents is required to run the SQL Analyzer Agent. "
        "Install with: pip install -e '.[dev]'"
    ) from exc


async def ask(question: str, *, model: str | None = None, db_path: Path | None = None) -> AnalysisAnswer:
    context = build_context(db_path)
    agent = build_agent(model=model)
    with trace("sql-analyzer-agent"):
        result = await Runner.run(
            agent,
            question,
            context=context,
            run_config=build_run_config(),
        )

    output = result.final_output
    if isinstance(output, AnalysisAnswer):
        return output
    return AnalysisAnswer.model_validate(output)


def _format_answer(answer: AnalysisAnswer) -> str:
    lines = [
        f"Question: {answer.question}",
        "",
        "SQL:",
        answer.sql,
        "",
        "Rows:",
    ]
    for row in answer.rows:
        if len(row) == len(answer.columns):
            lines.append(f"- {dict(zip(answer.columns, row, strict=True))}")
        else:
            lines.append(f"- {row}")
    lines.extend(["", "Explanation:", answer.explanation])
    if answer.caveats:
        lines.extend(["", "Caveats:"])
        lines.extend(f"- {item}" for item in answer.caveats)
    return "\n".join(lines)


async def async_main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Ask the SQL Analyzer Agent one business question.")
    parser.add_argument("question", help="Natural-language business question.")
    parser.add_argument("--model", default=None, help="Override the model for this run.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path.")
    args = parser.parse_args(argv)

    db_path = Path(args.db_path).expanduser().resolve() if args.db_path else None
    answer = await ask(args.question, model=args.model, db_path=db_path)
    print(_format_answer(answer))
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(async_main()))


if __name__ == "__main__":
    main()
