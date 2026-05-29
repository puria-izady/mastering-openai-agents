from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")


@dataclass(frozen=True)
class TextStats:
    line_count: int
    word_count: int
    top_words: list[tuple[str, int]]


def normalize_words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def analyze_text(text: str, *, top_n: int = 5) -> TextStats:
    words = normalize_words(text)
    return TextStats(
        line_count=0 if text == "" else text.count("\n") + 1,
        word_count=len(words),
        top_words=Counter(words).most_common(top_n),
    )

