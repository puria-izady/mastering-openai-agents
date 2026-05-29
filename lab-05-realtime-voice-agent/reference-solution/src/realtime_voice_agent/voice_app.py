from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from agents import Agent
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    SingleAgentWorkflowCallbacks,
    VoicePipeline,
    VoicePipelineConfig,
)

from .agent import build_voice_agent
from .config import (
    DEFAULT_STT_MODEL,
    DEFAULT_TTS_MODEL,
    TRACE_METADATA,
    TRACE_WORKFLOW_NAME,
)


@dataclass
class TranscriptCapture(SingleAgentWorkflowCallbacks):
    transcriptions: list[str] = field(default_factory=list)

    def on_run(self, workflow: SingleAgentVoiceWorkflow, transcription: str) -> None:
        del workflow
        self.transcriptions.append(transcription)


def build_voice_pipeline(
    agent: Agent | None = None,
    *,
    callbacks: TranscriptCapture | None = None,
    stt_model: str = DEFAULT_STT_MODEL,
    tts_model: str = DEFAULT_TTS_MODEL,
) -> VoicePipeline:
    workflow = SingleAgentVoiceWorkflow(
        agent or build_voice_agent(),
        callbacks=callbacks or TranscriptCapture(),
    )
    config = VoicePipelineConfig(
        workflow_name=TRACE_WORKFLOW_NAME,
        trace_metadata=TRACE_METADATA,
        trace_include_sensitive_audio_data=False,
    )
    return VoicePipeline(
        workflow=workflow,
        stt_model=stt_model,
        tts_model=tts_model,
        config=config,
    )


def make_silence_audio(seconds: float = 1.0, sample_rate: int = 24_000) -> AudioInput:
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    sample_count = int(seconds * sample_rate)
    return AudioInput(buffer=np.zeros(sample_count, dtype=np.int16))


def record_microphone_audio(seconds: float = 3.0, sample_rate: int = 24_000) -> AudioInput:
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    try:
        import sounddevice as sd
    except ImportError as exc:
        raise RuntimeError(
            "Microphone recording requires the optional mic dependencies. "
            "Install them with: uv sync --extra dev --extra mic. "
            "Then run with: uv run --extra mic python run_reference.py --record --seconds 4"
        ) from exc

    sample_count = int(seconds * sample_rate)
    print(f"Recording microphone for {seconds:g} seconds...")
    recording = sd.rec(sample_count, samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    return AudioInput(buffer=recording.reshape(-1))


class AudioPlayback:
    def __init__(self, sample_rate: int = 24_000):
        self.sample_rate = sample_rate
        self._stream: Any | None = None

    def __enter__(self) -> AudioPlayback:
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError(
                "Audio playback requires the optional mic dependencies. "
                "Install them with: uv sync --extra dev --extra mic. "
                "Then run with: uv run --extra mic python run_reference.py --record --seconds 4"
            ) from exc

        self._stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16,
        )
        self._stream.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()

    def add_audio(self, audio_data: Any) -> None:
        if self._stream is not None and audio_data is not None:
            self._stream.write(audio_data.reshape(-1))


def summarize_voice_event(event: Any) -> str:
    event_type = getattr(event, "type", type(event).__name__)
    if event_type == "voice_stream_event_audio":
        data = getattr(event, "data", None)
        samples = int(getattr(data, "size", 0)) if data is not None else 0
        return f"audio samples={samples}"
    if event_type == "voice_stream_event_lifecycle":
        return f"lifecycle event={getattr(event, 'event', 'unknown')}"
    if event_type == "voice_stream_event_error":
        return f"error {getattr(event, 'error', 'unknown')}"
    return event_type
