from __future__ import annotations

import argparse
from pathlib import Path

from text_stats.cli import format_stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Lab 00 text-stats reference demo.")
    parser.add_argument("path", type=Path, help="Text file to analyze.")
    args = parser.parse_args()
    print(format_stats(args.path))


if __name__ == "__main__":
    main()
