from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline

from realtime_voice_agent.config import TRACE_METADATA, TRACE_WORKFLOW_NAME
from realtime_voice_agent.voice_app import (
    AudioPlayback,
    TranscriptCapture,
    build_voice_pipeline,
    make_silence_audio,
    record_microphone_audio,
    summarize_voice_event,
)


def test_make_silence_audio_returns_static_audio_input() -> None:
    audio = make_silence_audio(seconds=0.25, sample_rate=8_000)

    assert isinstance(audio, AudioInput)
    assert audio.buffer.dtype == np.int16
    assert audio.buffer.shape == (2_000,)
    assert np.all(audio.buffer == 0)


@pytest.mark.parametrize("seconds,sample_rate", [(0, 24_000), (1, 0)])
def test_make_silence_audio_validates_inputs(seconds: float, sample_rate: int) -> None:
    with pytest.raises(ValueError):
        make_silence_audio(seconds=seconds, sample_rate=sample_rate)


def test_build_voice_pipeline_returns_real_sdk_pipeline() -> None:
    callbacks = TranscriptCapture()

    pipeline = build_voice_pipeline(callbacks=callbacks)

    assert isinstance(pipeline, VoicePipeline)
    assert isinstance(pipeline.workflow, SingleAgentVoiceWorkflow)
    assert pipeline.config.workflow_name == TRACE_WORKFLOW_NAME
    assert pipeline.config.trace_metadata == TRACE_METADATA
    assert pipeline.config.trace_include_sensitive_audio_data is False


def test_transcript_capture_records_workflow_input() -> None:
    callbacks = TranscriptCapture()

    callbacks.on_run(SimpleNamespace(), "What should I inspect in traces?")

    assert callbacks.transcriptions == ["What should I inspect in traces?"]


def test_summarize_voice_event_handles_lifecycle_and_audio() -> None:
    lifecycle = SimpleNamespace(type="voice_stream_event_lifecycle", event="turn_started")
    audio = SimpleNamespace(type="voice_stream_event_audio", data=np.zeros(4, dtype=np.int16))
    unknown = SimpleNamespace(type="custom")

    assert summarize_voice_event(lifecycle) == "lifecycle event=turn_started"
    assert summarize_voice_event(audio) == "audio samples=4"
    assert summarize_voice_event(unknown) == "custom"


def test_record_microphone_audio_validates_inputs() -> None:
    with pytest.raises(ValueError):
        record_microphone_audio(seconds=0)


def test_audio_playback_stores_sample_rate() -> None:
    playback = AudioPlayback(sample_rate=16_000)

    assert playback.sample_rate == 16_000
