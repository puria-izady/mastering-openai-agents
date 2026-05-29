from text_stats.core import analyze_text, normalize_words


def test_normalize_words_handles_punctuation() -> None:
    assert normalize_words("Hello, HELLO! Team.") == ["hello", "hello", "team"]


def test_analyze_empty_text() -> None:
    stats = analyze_text("")
    assert stats.line_count == 0
    assert stats.word_count == 0
    assert stats.top_words == []


def test_analyze_repeated_words() -> None:
    stats = analyze_text("Agent agent tool\nTool")
    assert stats.line_count == 2
    assert stats.word_count == 4
    assert stats.top_words[:2] == [("agent", 2), ("tool", 2)]

