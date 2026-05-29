from __future__ import annotations

from pathlib import Path

from agents import Agent, Runner, SQLiteSession

from .run_config import build_run_config


def build_agent(model: str = "gpt-5.5") -> Agent:
    return Agent(
        name="Preference assistant",
        instructions="Remember the user's preferences across turns when a session is provided.",
        model=model,
    )


def build_session(session_id: str, db_path: Path | str = ":memory:") -> SQLiteSession:
    return SQLiteSession(session_id, db_path=db_path)


async def ask_with_session(question: str, session: SQLiteSession) -> str:
    result = await Runner.run(build_agent(), question, session=session, run_config=build_run_config())
    return str(result.final_output)
