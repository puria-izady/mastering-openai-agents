# Lab 05 Prompt Pack: Realtime Voice Agent

Default all SDK Agent/SandboxAgent model settings to `gpt-6-luna`. Keep modality-specific transcription, speech, and realtime audio model IDs unchanged.

Use this prompt pack to rebuild the Lab 05 reference solution from scratch in
`lab-05-realtime-voice-agent/reference-solution/`.

Before starting, read:

- `AGENTS.md`
- `replay-environment/.agents/skills/openai-agents-sdk/SKILL.md`
- `replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/examples/voice/`

Use the OpenAI Docs MCP to verify current guidance for Python voice agents.
Record the official URLs and the guidance you relied on in the generated
solution.

## Implementation Requirements

Preserve these behavior requirements when rebuilding or revising the lab:

- `--seconds` alone must not imply microphone capture. It should submit
  generated silence as static `AudioInput` and print that clearly.
- Real microphone capture must require `--record`; otherwise you cannot
  tell whether the pipeline captured microphone input or only processed silence.
- For optional microphone dependencies, document `uv sync --extra dev --extra
  mic` and run with `uv run --extra mic ...`. A plain `uv pip install -e
  '.[dev,mic]'` can leave `sounddevice` absent from the environment used by
  `uv run`.
- When `--record` is used, print the transcription captured by
  `SingleAgentWorkflowCallbacks`; this is the quickest way to verify what STT
  heard.
- TTS output arrives as `voice_stream_event_audio` chunks. Printing sample
  counts proves audio was produced, but you will not hear a response unless
  the demo writes those chunks to an output stream.
- `--record` should play response audio by default, and `--no-playback` should
  disable speakers for CI, classrooms, or silent environments.
- Disable sensitive audio payload tracing with
  `trace_include_sensitive_audio_data=False` while keeping workflow tracing and
  metadata enabled. This avoids non-fatal invalid audio payload trace export
  errors while preserving useful traces.
- The true realtime solution is a separate TypeScript/browser architecture:
  `RealtimeAgent` + `RealtimeSession` over WebRTC, with a trusted server
  minting ephemeral realtime client secrets. Do not present Python
  `VoicePipeline` as the realtime-agent solution.
- For realtime browser logging, do not spam `history_updated`. Log transport
  events that show what happened: input audio transcription completed,
  assistant output audio transcript delta/done, response done, audio start/stop,
  interruptions, and errors.
- Configure input audio transcription explicitly so you can see `You said:
  ...` in the UI.
- Do not log assistant transcript deltas as final answers; log only the
  completed assistant transcript to avoid making one response look like many
  responses.
- Do not log SDK `agent_end` output as a second visible assistant answer when
  the transport transcript already logs `Assistant said: ...`.
- Suppress empty input transcription logs and tune semantic VAD with low
  eagerness to reduce empty/noisy turns that repeat prior answers.
- A `RealtimeAgent` + `RealtimeSession` browser app is already the realtime
  voice-agent approach. Do not add a separate `VoicePipeline`, STT, or TTS layer
  inside the browser realtime app.
- If a single answer appears twice in the UI, first check logging. The SDK can
  expose the same turn through transport transcript events, audio events, and
  agent lifecycle events. The user-facing status panel should choose one
  completed assistant transcript as the visible answer.

## Prompt 1: Scaffold The Python Project

Create a Python project in `lab-05-realtime-voice-agent/reference-solution/`.

Requirements:

- Use package name `realtime_voice_agent`.
- Add `pyproject.toml` with `openai-agents[voice]`, `numpy`, `pytest`, and
  `pytest-asyncio`.
- Add an optional `mic` dependency group with `sounddevice` for microphone
  capture.
- Add `README.md`, `.env.example`, `.gitignore`, `run_reference.py`, `tests/`,
  and `BUILD-LOG.md`.
- Add a docs note that cites the OpenAI voice agents guide and audio guide.
- Explain in the README that Python voice-agent reuse should use SDK
  `VoicePipeline`, while browser speech-to-speech realtime sessions are a
  different JavaScript/transport path.
- In the README, use `uv sync --extra dev` for setup and `uv sync --extra dev
  --extra mic` for microphone support.
- Do not make API calls in tests.

Verification:

- Run local tests if any exist.
- Record the command and result in `BUILD-LOG.md`.

## Prompt 2: Add The Voice Agent And Tool

Add a direct SDK `Agent` definition.

Requirements:

- Define `build_voice_agent() -> Agent`.
- Use a function-call-safe agent name such as `voice_course_assistant`.
- Add a deterministic `@function_tool` named `lookup_lab_answer`.
- The tool should return a small deterministic lookup result for topics such as
  `voicepipeline`, `traces`, and `tools`.
- Tool names must use only lowercase letters, digits, and underscores.
- Keep the SDK `Agent` and `@function_tool` visible to you.

Verification:

- Add local tests that assert `build_voice_agent()` returns a real SDK `Agent`.
- Add tests that assert the tool name is function-call safe.
- Add tests for the deterministic lookup helper without making API calls.

## Prompt 3: Add The Voice Pipeline

Add the Python Agents SDK voice workflow.

Requirements:

- Use SDK `AudioInput`, `VoicePipeline`, `VoicePipelineConfig`,
  `SingleAgentVoiceWorkflow`, and `SingleAgentWorkflowCallbacks`.
- Define `build_voice_pipeline()` that returns a real SDK `VoicePipeline`.
- Configure `workflow_name="lab-05-realtime-voice-agent"` and trace metadata.
- Add a `TranscriptCapture` callback that records transcriptions locally.
- Add `make_silence_audio()` that returns a static `AudioInput` using a
  deterministic NumPy `int16` buffer.
- Add optional `record_microphone_audio()` that records microphone input for a
  fixed number of seconds and returns a static `AudioInput`.
- If `sounddevice` is missing, raise an error that tells you to run
  `uv sync --extra dev --extra mic` and then `uv run --extra mic python
  run_reference.py --record --seconds 4`.
- Add `summarize_voice_event()` so the runnable demo can print lifecycle and
  audio stream events.
- Add optional response audio playback for microphone runs, plus a way to
  disable playback for CI or classroom environments.
- Disable sensitive audio payload tracing in `VoicePipelineConfig` while
  keeping workflow name and trace metadata enabled.

Verification:

- Add local tests for pipeline construction, trace metadata, callbacks, audio
  buffer shape, and event summarization.
- Tests must not call STT, TTS, or a model.

## Prompt 4: Add The Runnable Demo

Add an API-backed runnable reference demo.

Requirements:

- `run_reference.py` should call the package CLI.
- The CLI should accept a `--seconds` flag for generated static audio length.
- The CLI should accept `--record` to capture microphone input for `--seconds`
  instead of using generated silence.
- The CLI should play response audio for `--record` runs by default and expose
  `--no-playback`.
- If `OPENAI_API_KEY` is absent, skip cleanly with exit code `0`.
- If `OPENAI_API_KEY` is present, build the SDK `VoicePipeline`, run it with a
  static `AudioInput`, and print summarized lifecycle/audio events.
- Print the transcription captured by `SingleAgentWorkflowCallbacks` so
  you can verify what speech-to-text heard.
- Print lifecycle/audio summaries and play the streamed response audio so
  you can tell that the agent responded.
- Print where you should inspect traces.
- Make the generated-silence path print a clear message such as: `Using
  generated silence as static AudioInput. Pass --record to capture microphone
  input.`
- Include the exact microphone command in README: `uv run --extra mic python
  run_reference.py --record --seconds 4`.
- Include the exact silent verification command in README: `uv run --extra mic
  python run_reference.py --record --seconds 4 --no-playback`.

Verification:

- Add a test for the clean skip path without `OPENAI_API_KEY`.
- Run the local tests.
- If no API key is available, run the demo and verify that it skips cleanly.

## Prompt 5: Finalize Lab Materials

Finalize the lab for replay.

Requirements:

- Update `README.md` with setup, test, demo, and tracing instructions.
- Update `BUILD-LOG.md` with each prompt ID and verification result.
- Keep the lab-level `labs/lab-05-realtime-voice-agent/prompt-pack.md`
  complete enough for replay; it must not rely on reading inside a
  `reference-solution/`.
- Use direct SDK objects. Do not hide the SDK behind course-specific runner,
  workflow, or base-agent abstractions.

Verification:

- Run all local tests.
- Confirm the API-backed demo skips cleanly without `OPENAI_API_KEY`.

## Prompt 6: Add The True Realtime Browser Agent

Add a sibling reference implementation in
`lab-05-realtime-voice-agent/reference-solution/realtime-browser/`.

Requirements:

- Use the TypeScript OpenAI Agents SDK package `@openai/agents`.
- Use SDK `RealtimeAgent` and `RealtimeSession` from
  `@openai/agents/realtime`.
- Use model `gpt-realtime-2`.
- Use a function-call-safe realtime agent name such as
  `realtime_course_assistant`.
- Add a browser UI that starts and stops a realtime session, requests
  microphone permission, and lets you send an optional text event.
- The browser UI should log useful runtime events, including `You said: ...`,
  `Assistant said: ...`, `Assistant audio started`, and `Realtime turn
  complete`.
- The browser UI should suppress empty `You said:` lines and should not show
  every assistant transcript delta as a separate status entry.
- Do not log every `history_updated` event; it produces noisy output and hides
  the useful transcript/debug signals.
- Add a trusted Node/Express `/token` server endpoint that calls
  `https://api.openai.com/v1/realtime/client_secrets`.
- Keep the standard `OPENAI_API_KEY` only on the trusted server. The browser
  must receive only the ephemeral realtime client secret.
- Include an `OpenAI-Safety-Identifier` header on the server-side client secret
  request.
- Use HTTPS for the browser dev server, because microphone access requires
  HTTPS or localhost.
- Explain that this realtime app is not the Python `VoicePipeline`: it keeps a
  live WebRTC session open and the model handles the speech-to-speech
  conversation directly.
- Do not combine the realtime browser app with the Python voice pipeline. They
  are two alternate architectures in the same lab, not layers of one runtime.

Verification:

- Add local tests that construct the realtime agent/session without connecting.
- Add local tests for client-secret response parsing and server token request
  construction.
- Run `npm test`.
- Run `npm run typecheck`.
- Run `npm run build`.
- Do not call the OpenAI API in local tests.

## Prompt 7: Polish Realtime Browser Runtime Behavior

Verify the live browser runtime behavior before sharing the lab.

Requirements:

- Confirm the app shows the user's speech transcript from
  `conversation.item.input_audio_transcription.completed`.
- Confirm the app shows assistant transcript output from
  `response.output_audio_transcript.delta` or
  `response.output_audio_transcript.done`.
- Confirm the app logs audio start/stop and response completion.
- Confirm a single spoken answer appears as one completed `Assistant said: ...`
  line, not a stream of word-piece deltas plus a duplicate `agent_end` line.
- Treat duplicate visible answers as a UI event-logging bug unless the raw
  realtime transcript clearly shows two separate model turns.
- Confirm empty input audio transcription events are ignored in the status
  panel.
- Use `semantic_vad` with low eagerness for this lab app so short pauses
  and background noise are less likely to create empty turns.
- Make the realtime agent instruction robust against unclear audio. It should
  not claim to read the user's mind; it should answer only spoken or typed
  content and ask the user to repeat unclear input.
- Keep the standard API key server-side and keep the browser using only the
  ephemeral realtime client secret.

Verification:

- Run `npm test`.
- Run `npm run typecheck`.
- Run `npm run build`.
- Manually run the browser app and confirm the status panel includes `You said:
  ...` and `Assistant said: ...`.
- During browser verification, ask a multi-turn sequence such as `Can you hear me?`,
  `What is the capital of Germany?`, and `What is the capital of Slovenia?`.
  Confirm each real user turn produces one visible completed assistant answer.
