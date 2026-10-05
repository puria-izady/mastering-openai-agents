from __future__ import annotations

from agents import Agent, Runner

from .models import CalendarEvent
from .run_config import build_run_config


def build_agent(model: str = "gpt-6-luna") -> Agent:
    return Agent(
        name="Calendar extractor",
        instructions="Extract one calendar event from the user's message.",
        model=model,
        output_type=CalendarEvent,
    )


async def extract_event(text: str) -> CalendarEvent:
    result = await Runner.run(build_agent(), text, run_config=build_run_config())
    return CalendarEvent.model_validate(result.final_output)
