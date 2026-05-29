from __future__ import annotations

from agents import Agent

from realtime_voice_agent.agent import build_voice_agent, lookup_lab_answer_record


def test_build_voice_agent_returns_real_sdk_agent() -> None:
    agent = build_voice_agent(model="gpt-5-mini")

    assert isinstance(agent, Agent)
    assert agent.name == "voice_course_assistant"
    assert agent.model == "gpt-5-mini"


def test_tool_name_is_function_call_safe() -> None:
    agent = build_voice_agent()
    tool_names = [tool.name for tool in agent.tools]

    assert "lookup_lab_answer" in tool_names
    assert all(name.replace("_", "").isalnum() for name in tool_names)
    assert all(name == name.lower() for name in tool_names)


def test_lookup_lab_answer_record_is_deterministic() -> None:
    first = lookup_lab_answer_record("VoicePipeline")
    second = lookup_lab_answer_record("voicepipeline")

    assert first == second
    assert first.source == "OpenAI voice agents guide"
    assert "speech-to-text" in first.answer
