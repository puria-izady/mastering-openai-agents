# Realtime Browser Agent

This is the true realtime variant of Lab 05. It is intentionally separate from
the Python `VoicePipeline` example.

Use this path when the application should feel conversational and immediate:
browser microphone input, WebRTC transport, barge-in, low first-audio latency,
and live audio output.

## Architecture

- Browser: OpenAI Agents SDK `RealtimeAgent` and `RealtimeSession`.
- Server: trusted Node/Express endpoint that mints a realtime client secret.
- Transport: WebRTC handled by the SDK session.
- Model: `gpt-realtime-2`.

The standard OpenAI API key must stay on the server. The browser receives only a
short-lived realtime client secret from `/token`.

## Run Local Tests

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution/realtime-browser
npm install
npm test
npm run typecheck
```

Tests construct SDK realtime objects and validate token request configuration
without calling OpenAI.

## Run The Realtime Demo

Terminal 1:

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution/realtime-browser
export OPENAI_API_KEY='sk-...'
npm run server
```

Terminal 2:

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution/realtime-browser
npm run dev
```

Open the HTTPS Vite URL printed by `npm run dev`, usually
`https://127.0.0.1:5173`. Browser microphone access generally requires HTTPS or
localhost.

Click **Start realtime session**, allow microphone access, and speak. You should
hear the model respond through the browser audio output.

The status panel should show useful checkpoints such as:

- `You said: ...`
- `Assistant audio started.`
- `Assistant said: ...`
- `Realtime turn complete.`

## Why This Is Not The Python VoicePipeline

The Python solution is a chained workflow: speech-to-text, text agent run, then
text-to-speech. This realtime solution keeps a live session open and lets the
model handle the audio conversation directly through `RealtimeSession`.

## Official References

- Voice agents guide:
  <https://developers.openai.com/api/docs/guides/voice-agents>
- Realtime and audio guide:
  <https://developers.openai.com/api/docs/guides/realtime>
- Realtime WebRTC guide:
  <https://developers.openai.com/api/docs/guides/realtime-webrtc>
