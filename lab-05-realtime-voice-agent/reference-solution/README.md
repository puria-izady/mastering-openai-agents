# Lab 05: Realtime Voice Agent

This reference solution teaches the Python voice-agent path in the OpenAI
Agents SDK. The lab uses a chained voice workflow:

1. speech-to-text transcribes audio input,
2. a normal SDK `Agent` handles the text workflow and tools,
3. text-to-speech streams spoken output.

The OpenAI voice agents guide distinguishes this Python path from browser
speech-to-speech sessions. Browser/mobile realtime agents usually start with
TypeScript `RealtimeAgent` and `RealtimeSession`; Python text-agent reuse starts
with `VoicePipeline`.

## Project Pieces

- `src/realtime_voice_agent/agent.py` defines a real SDK `Agent` and a
  deterministic `@function_tool`.
- `src/realtime_voice_agent/voice_app.py` builds a real SDK `VoicePipeline`
  with `SingleAgentVoiceWorkflow`.
- `run_reference.py` runs the API-backed demo and skips cleanly without
  `OPENAI_API_KEY`.
- `realtime-browser/` contains the true realtime browser implementation using
  the TypeScript Agents SDK `RealtimeAgent` and `RealtimeSession`.
- `tests/` verifies SDK object contracts without making model calls.

Tool names intentionally use only lowercase letters, digits, and underscores so
the SDK does not need to transform them for function calling.

## Setup

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution
uv sync --extra dev
```

To try real microphone input, install the optional microphone dependency:

```bash
uv sync --extra dev --extra mic
```

If you are running from the replay environment and want to use the bundled SDK
checkout directly:

```bash
uv pip install -e '../../replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python[voice]'
uv pip install -e '.[dev]' --no-deps
```

## Run Tests

```bash
uv run pytest
```

The tests are local contract tests. They do not call the OpenAI API and they do
not require a microphone.

## Run The Demo

### Python Voice Pipeline

```bash
export OPENAI_API_KEY='sk-...'
uv run python run_reference.py --seconds 1
```

Without `OPENAI_API_KEY`, the command exits successfully and prints a skip
message. With a key, the default command builds a static `AudioInput` from
generated silence, runs the `VoicePipeline`, and prints lifecycle/audio stream
summaries. This proves the pipeline is wired, but it does not capture your
voice.

To capture microphone input:

```bash
uv run --extra mic python run_reference.py --record --seconds 4
```

The command prints the transcription captured by
`SingleAgentWorkflowCallbacks`, so you can verify what the speech-to-text stage
heard before the agent responded. It also plays the response audio streamed by
the SDK `VoicePipeline`.

To capture and transcribe without playing the response audio:

```bash
uv run --extra mic python run_reference.py --record --seconds 4 --no-playback
```

### Browser Realtime Agent

The browser realtime solution is the live speech-to-speech architecture. It is
not a chained `VoicePipeline`; it uses a browser `RealtimeSession` over WebRTC.

```bash
cd realtime-browser
npm install
npm test
npm run typecheck
npm run build
```

Run the trusted token server:

```bash
export OPENAI_API_KEY='sk-...'
npm run server
```

In another terminal:

```bash
npm run dev
```

Open the HTTPS Vite URL, usually `https://127.0.0.1:5173`, click **Start
realtime session**, allow microphone access, and speak. The browser receives
only an ephemeral realtime client secret from the local `/token` endpoint; the
standard OpenAI API key stays on the server.

## Traces

Inspect traces in the OpenAI dashboard. The pipeline sets
`workflow_name="lab-05-realtime-voice-agent"` and trace metadata for the course,
lab number, and voice surface. The reference solution disables sensitive audio
payload tracing while keeping the workflow trace metadata visible.

## Official References

- OpenAI voice agents guide:
  <https://developers.openai.com/api/docs/guides/voice-agents>
- OpenAI audio guide:
  <https://developers.openai.com/api/docs/guides/audio>
- OpenAI realtime WebRTC guide:
  <https://developers.openai.com/api/docs/guides/realtime-webrtc>
- Local SDK examples:
  `replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/examples/voice/`
