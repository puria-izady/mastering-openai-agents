# Build Log

## Prompt 1: Scaffold Lab 05 Python Project

Created a Python package for a realtime voice agent lab using the OpenAI Agents
SDK voice surface.

Verification:

- `uv run pytest`
  passed.

## Prompt 2: Agent And Deterministic Tool

Added `build_voice_agent()` with a real SDK `Agent` and a deterministic
`lookup_lab_answer` function tool.

Verification:

- Local tests cover SDK `Agent` construction and function-call-safe tool names.
- `uv run pytest`
  passed.

## Prompt 3: Voice Pipeline

Added `build_voice_pipeline()` using SDK `VoicePipeline`,
`SingleAgentVoiceWorkflow`, `VoicePipelineConfig`, and static `AudioInput`
generation.

Verification:

- Local tests cover pipeline construction, trace metadata, transcript callback,
  generated audio buffer shape, and stream event summarization.
- `uv run pytest`
  passed.

## Prompt 4: API-Backed Demo

Added `run_reference.py` and CLI entrypoint. The demo skips cleanly when
`OPENAI_API_KEY` is absent.

Verification:

- Local test covers the skip behavior without making an API call.
- `uv run python run_reference.py --seconds 0.1`
  skipped cleanly without `OPENAI_API_KEY`.
- Updated the CLI so the default `--seconds` path clearly uses generated
  silence and `--record` captures microphone input when optional mic
  dependencies are installed.
- Disabled sensitive audio payload tracing to avoid non-fatal invalid audio
  trace payload errors while preserving workflow tracing metadata.
- Updated microphone setup instructions to use `uv sync --extra dev --extra mic`
  and `uv run --extra mic ...`, so the optional `sounddevice` dependency is
  present in the environment used by `uv run`.
- Added response audio playback for `--record` runs and `--no-playback` for
  environments where speakers are unavailable.

## Prompt 5: Docs And Replay Pack

Added README instructions and OpenAI Docs verification notes.

Verification:

- `uv run pytest`
  passed with 12 tests.

## Prompt 6: Realtime Browser Agent

Added a second reference implementation in `realtime-browser/` for the true
realtime voice-agent architecture.

Implementation:

- TypeScript Agents SDK `RealtimeAgent` and `RealtimeSession`.
- Trusted Node/Express `/token` endpoint that mints an ephemeral realtime client
  secret with the standard `OPENAI_API_KEY` kept server-side.
- Browser UI for microphone capture and live WebRTC session connection.
- Local tests for realtime agent naming, session config, client secret parsing,
  and token request construction.

Verification:

- `npm test` passed with 6 tests.
- `npm run typecheck` passed.
- `npm run build` passed.

## Prompt 7: Realtime Browser Runtime Logging Fix

Runtime verification confirmed that the realtime UI should surface transport
events directly so you can see what the model heard and when a turn
completed.

Fixes:

- Removed noisy `history_updated` logging from the UI.
- Added transport event logging for input audio transcription and assistant
  output audio transcripts.
- Added `audio_start`, `audio_stopped`, `audio_interrupted`, `agent_start`, and
  `agent_end` status messages.
- Made input transcription and semantic VAD explicit in both the server session
  config and `RealtimeSession` options.
- Tightened the realtime agent instructions: respond only to spoken or typed
  content, never claim to read minds, and ask the user to repeat unclear audio.
- Removed `agent_end` as a user-visible answer log because it duplicated the
  completed assistant transcript.
- Stopped logging assistant transcript deltas as standalone status lines.
- Suppressed empty input transcription logs and changed semantic VAD eagerness
  from `auto` to `low`.

Verification:

- `npm test` passed with 6 tests.
- `npm run typecheck` passed.
- `npm run build` passed.


## 2026-10-05 — GPT-6 Luna default update

Updated text/sandbox agent defaults to `gpt-6-luna` and verified SDK model
contracts locally. Explicit model overrides remain available; dedicated
transcription, speech, and realtime models are unchanged.

Local pytest suite: **12 passed**, using openai-agents 0.17.3.
API credentials were removed from the test environment. No live model calls
were made; this verifies configuration and local behavior, not live API access.
No-key demo check: skipped API execution successfully (exit 0).
