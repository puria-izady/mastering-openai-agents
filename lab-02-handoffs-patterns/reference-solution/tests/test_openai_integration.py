from __future__ import annotations

import asyncio
import os

import pytest

from handoffs_patterns.agents_as_tools import run_manager
from handoffs_patterns.agents_handoff import run_handoff


def _require_openai_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    if os.getenv("REQUIRE_OPENAI_API") == "1":
        pytest.fail("OPENAI_API_KEY is required for OpenAI integration tests.")
    pytest.skip("OPENAI_API_KEY is not set.")


def test_agents_as_tools_calls_openai_api() -> None:
    _require_openai_key()
    output = asyncio.run(run_manager("My invoice is higher and export is broken."))
    assert output.strip()


def test_handoff_calls_openai_api() -> None:
    _require_openai_key()
    output, last_agent = asyncio.run(run_handoff("The export button fails with a 500 error."))
    assert output.strip()
    assert last_agent
