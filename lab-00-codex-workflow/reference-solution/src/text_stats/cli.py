from __future__ import annotations

import argparse
from pathlib import Path

from .core import analyze_text


def format_stats(path: Path) -> str:
    stats = analyze_text(path.read_text(encoding="utf-8"))
    lines = [
        f"file: {path}",
        f"lines: {stats.line_count}",
        f"words: {stats.word_count}",
        "top_words:",
    ]
    lines.extend(f"- {word}: {count}" for word, count in stats.top_words)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Print basic text statistics.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    print(format_stats(args.path))

