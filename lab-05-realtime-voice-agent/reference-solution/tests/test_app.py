from __future__ import annotations

import pytest

from realtime_voice_agent.app import run_demo


@pytest.mark.asyncio
async def test_run_demo_skips_without_api_key(monkeypatch, capsys) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    exit_code = await run_demo(seconds=0.1)

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Skipping API-backed voice demo" in output
    assert "OPENAI_API_KEY" in output
