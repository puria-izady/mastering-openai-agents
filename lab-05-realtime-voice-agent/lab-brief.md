# Lab 05 Brief: Realtime Voice Agent

## Goal

Build a Python voice-agent reference solution with the OpenAI Agents SDK.

You learn how to reuse a normal SDK `Agent` inside a chained voice
pipeline that explicitly handles speech-to-text, agent reasoning, and
text-to-speech.

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

## Local Verification

Local tests validate SDK object contracts and deterministic helpers without
making API calls or using audio hardware.
