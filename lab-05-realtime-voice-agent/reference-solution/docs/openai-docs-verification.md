# OpenAI Docs Verification

Checked with the OpenAI Docs MCP while building this lab.

## Voice Agents Guide

URL: <https://developers.openai.com/api/docs/guides/voice-agents>

Relevant guidance:

- Voice agents are SDK-first.
- Choose between speech-to-speech live audio sessions and chained voice
  pipelines.
- Python's simplest path for extending a text agent into voice is
  `VoicePipeline`.
- The voice surface still uses the same core agent building blocks: tools,
  running agents, handoffs, guardrails, and observability.

## Audio Guide

URL: <https://developers.openai.com/api/docs/guides/audio>

Relevant guidance:

- Browser live speech-to-speech starts with a JavaScript realtime session.
- Python voice workflows should use the voice agents guide and chained voice
  pipelines.

## Realtime WebRTC Guide

URL: <https://developers.openai.com/api/docs/guides/realtime-webrtc>

Relevant guidance:

- Browser and mobile realtime audio should use WebRTC for more consistent
  performance.
- A trusted server should create an ephemeral realtime client secret; the
  standard OpenAI API key must not be used in the browser.
- Browser clients can connect with a realtime session and handle microphone and
  speaker audio through the session transport.

## Realtime With Tools Guide

URL: <https://developers.openai.com/api/docs/guides/realtime-mcp>

Relevant guidance:

- Realtime sessions can use tools during a live conversation.
- Function tools are executed by the application and returned with
  `function_call_output`; MCP tools can be executed by the Realtime API.

## Local SDK Checkout

Path:

```text
replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/examples/voice/
```

Relevant SDK objects used here:

- `AudioInput`
- `SingleAgentVoiceWorkflow`
- `SingleAgentWorkflowCallbacks`
- `VoicePipeline`
- `VoicePipelineConfig`
