# Lab 05 Brief: Realtime Voice Agent

## Goal

Build a Python voice-agent reference solution with the OpenAI Agents SDK.

You learn how to reuse a normal SDK `Agent` inside a chained voice
pipeline that explicitly handles speech-to-text, agent reasoning, and
text-to-speech.

The lab also includes a TypeScript browser realtime reference solution using
`RealtimeAgent` and `RealtimeSession` for true speech-to-speech interactions
over WebRTC.

## Concepts

- `Agent`
- `@function_tool`
- `AudioInput`
- `VoicePipeline`
- `VoicePipelineConfig`
- `SingleAgentVoiceWorkflow`
- `SingleAgentWorkflowCallbacks`
- tracing workflow names and metadata
- API-backed demo skip behavior
- `RealtimeAgent`
- `RealtimeSession`
- browser WebRTC voice sessions
- ephemeral realtime client secrets

## Local Verification

Local tests validate SDK object contracts and deterministic helpers without
making API calls or using audio hardware.

The realtime browser app has separate `npm test`, `npm run typecheck`, and
`npm run build` verification.
