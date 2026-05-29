from __future__ import annotations

import argparse
import asyncio
from contextlib import nullcontext

from .config import has_openai_api_key
from .voice_app import (
    AudioPlayback,
    TranscriptCapture,
    build_voice_pipeline,
    make_silence_audio,
    record_microphone_audio,
    summarize_voice_event,
)


async def run_demo(seconds: float, *, record: bool = False, playback: bool = False) -> int:
    if not has_openai_api_key():
        print("Skipping API-backed voice demo: OPENAI_API_KEY is not set.")
        print("Local tests still validate Agent, tool, AudioInput, and VoicePipeline contracts.")
        return 0

    callbacks = TranscriptCapture()
    pipeline = build_voice_pipeline(callbacks=callbacks)
    if record:
        audio_input = record_microphone_audio(seconds=seconds)
    else:
        print(
            "Using generated silence as static AudioInput. "
            "Pass --record to capture microphone input."
        )
        audio_input = make_silence_audio(seconds=seconds)
    result = await pipeline.run(audio_input)

    playback_context = AudioPlayback() if playback else nullcontext(None)
    with playback_context as player:
        if playback:
            print("Playing response audio...")
        async for event in result.stream():
            print(summarize_voice_event(event))
            if (
                player is not None
                and getattr(event, "type", None) == "voice_stream_event_audio"
            ):
                player.add_audio(event.data)

    if callbacks.transcriptions:
        print("Transcription:")
        for transcription in callbacks.transcriptions:
            print(f"- {transcription}")

    print("Inspect traces in the OpenAI dashboard for workflow lab-05-realtime-voice-agent.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Lab 05 realtime voice agent demo.")
    parser.add_argument(
        "--seconds",
        type=float,
        default=1.0,
        help="Length of generated silence, or microphone capture when --record is used.",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help="Record microphone input for --seconds instead of generating silence.",
    )
    parser.add_argument(
        "--no-playback",
        action="store_true",
        help="Do not play response audio when --record is used.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return asyncio.run(
        run_demo(
            seconds=args.seconds,
            record=args.record,
            playback=args.record and not args.no_playback,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
