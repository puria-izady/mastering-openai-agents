from __future__ import annotations

from dataclasses import dataclass

from agents import Agent, function_tool

from .config import DEFAULT_MODEL


@dataclass(frozen=True)
class VoiceLabAnswer:
    topic: str
    answer: str
    source: str


_ANSWERS: dict[str, VoiceLabAnswer] = {
    "voicepipeline": VoiceLabAnswer(
        topic="voicepipeline",
        answer=(
            "Use VoicePipeline when you want explicit control over speech-to-text, "
            "the agent run, and text-to-speech."
        ),
        source="OpenAI voice agents guide",
    ),
    "traces": VoiceLabAnswer(
        topic="traces",
        answer=(
            "Inspect the run in the OpenAI traces dashboard; voice traces can include "
            "the transcript, tool calls, and audio playback when tracing is enabled."
        ),
        source="OpenAI Agents SDK voice examples",
    ),
    "tools": VoiceLabAnswer(
        topic="tools",
        answer=(
            "Voice agents use normal Agents SDK tools. Keep function tool names "
            "limited to lowercase letters, digits, and underscores."
        ),
        source="course SDK skill",
    ),
}


def normalize_topic(topic: str) -> str:
    return topic.strip().lower().replace(" ", "_").replace("-", "_")


def lookup_lab_answer_record(topic: str) -> VoiceLabAnswer:
    key = normalize_topic(topic)
    return _ANSWERS.get(
        key,
        VoiceLabAnswer(
            topic=key or "unknown",
            answer="No deterministic lab note is available for that topic.",
            source="local fixture",
        ),
    )


@function_tool(name_override="lookup_lab_answer")
def lookup_lab_answer(topic: str) -> str:
    """Return a deterministic lab note for a voice-agent course topic."""
    record = lookup_lab_answer_record(topic)
    return f"{record.answer} Source: {record.source}."


def build_voice_agent(model: str = DEFAULT_MODEL) -> Agent:
    return Agent(
        name="voice_course_assistant",
        model=model,
        instructions=(
            "You are a concise voice assistant for a course lab about the OpenAI "
            "Agents SDK. Answer in one or two spoken-friendly sentences. Use the "
            "lookup_lab_answer tool for questions about VoicePipeline, traces, or "
            "tool naming. Do not claim to have used a microphone unless audio input "
            "was actually provided by the pipeline."
        ),
        tools=[lookup_lab_answer],
    )
