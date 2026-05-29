from agents import Agent

from agents_sampler.function_tool_demo import LOOKUP, build_agent as build_tool_agent
from agents_sampler.guardrail_demo import classify_domain
from agents_sampler.models import CalendarEvent
from agents_sampler.run_config import build_run_config
from agents_sampler.session_demo import build_session
from agents_sampler.structured_extractor import build_agent as build_extractor


def test_calendar_event_schema() -> None:
    event = CalendarEvent(title="Review", date="2026-05-09", attendees=["Ada"])
    assert event.title == "Review"


def test_tool_lookup_is_deterministic() -> None:
    assert "workflows" in LOOKUP["pro"]


def test_agents_can_be_instantiated() -> None:
    assert isinstance(build_extractor(), Agent)
    tool_agent = build_tool_agent()
    assert isinstance(tool_agent, Agent)
    assert len(tool_agent.tools) == 1


def test_domain_classifier() -> None:
    assert classify_domain("How do handoffs work?").allowed
    assert not classify_domain("What is the best pizza dough?").allowed


def test_sqlite_session_can_be_constructed(tmp_path) -> None:
    session = build_session("student-1", tmp_path / "sessions.db")
    assert session.session_id == "student-1"


def test_run_config_is_visible_sdk_object() -> None:
    config = build_run_config()
    assert config.workflow_name == "lab-01-agents-sdk-sampler"
    assert config.trace_metadata["lab"] == "01"
