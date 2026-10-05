from __future__ import annotations

import os

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
DEFAULT_STT_MODEL = os.getenv("OPENAI_STT_MODEL", "gpt-4o-mini-transcribe")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
TRACE_WORKFLOW_NAME = "lab-05-realtime-voice-agent"
TRACE_METADATA = {
    "course": "mastering-openai-agents",
    "lab": "05",
    "surface": "voice_pipeline",
}


def has_openai_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))
