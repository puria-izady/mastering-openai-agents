from __future__ import annotations

import asyncio
import os

import pytest

from agents_sampler.first_agent import run_demo


def _require_openai_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    if os.getenv("REQUIRE_OPENAI_API") == "1":
        pytest.fail("OPENAI_API_KEY is required for OpenAI integration tests.")
    pytest.skip("OPENAI_API_KEY is not set.")


def test_first_agent_calls_openai_api() -> None:
    _require_openai_key()
    output = asyncio.run(run_demo("Reply with one short sentence about agent tools."))
    assert output.strip()
