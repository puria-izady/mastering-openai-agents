from __future__ import annotations

import asyncio
import os

import pytest
from agents import Runner

from sandbox_sampler.build_agent import build_sandbox_agent, build_unix_local_sandbox_run_config


def _require_openai_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    if os.getenv("REQUIRE_OPENAI_API") == "1":
        pytest.fail("OPENAI_API_KEY is required for OpenAI integration tests.")
    pytest.skip("OPENAI_API_KEY is not set.")


def test_sandboxagent_calls_openai_api_with_unixlocal() -> None:
    _require_openai_key()

    async def run() -> str:
        result = await Runner.run(
            build_sandbox_agent(),
            "Inspect the workspace and list the project files. Do not edit files.",
            run_config=build_unix_local_sandbox_run_config(),
            max_turns=8,
        )
        return str(result.final_output)

    assert asyncio.run(run()).strip()
