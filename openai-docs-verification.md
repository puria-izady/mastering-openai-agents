# OpenAI Docs Verification

Verification date: 2026-05-29

## Sources Checked

- OpenAI Docs MCP: `https://developers.openai.com/api/docs/guides/agents/quickstart`
- OpenAI Docs MCP: `https://developers.openai.com/api/docs/guides/agents/sandboxes`
- OpenAI Docs MCP: `https://developers.openai.com/api/docs/guides/voice-agents`
- OpenAI Docs MCP: `https://developers.openai.com/api/docs/guides/realtime-webrtc`
- Local official SDK checkout:
  `replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/docs/human_in_the_loop.md`
- Local official SDK examples:
  `replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/examples/sandbox/unix_local_runner.py`
  `replay-environment/.agents/skills/openai-agents-sdk/openai-agents-python/examples/agent_patterns/human_in_the_loop_custom_rejection.py`

## Confirmed Course Patterns

- Agents are defined with `Agent(...)` and executed with `Runner.run(...)`.
- Function tools use `@function_tool`.
- Specialist routing can use either handoffs or `Agent.as_tool(...)`.
- Per-run settings belong in `RunConfig`, including `workflow_name` and trace
  metadata.
- SandboxAgent keeps the normal agent surface but changes the execution
  boundary to a sandbox session. Sandbox-specific session choices belong in
  `RunConfig(sandbox=SandboxRunConfig(...))`.
- Unix-local sandbox references should use `UnixLocalSandboxClient` through
  `SandboxRunConfig`.
- Human approval flows use `needs_approval`, `result.interruptions`,
  `result.to_state()`, `state.approve(...)`, `state.reject(...)`, and resume
  with `Runner.run(agent, state, ...)`.

## Applied To Labs

- Lab 01: first agent, tools, guardrails, sessions, structured output,
  `RunConfig`.
- Lab 02: handoffs and agents-as-tools.
- Lab 03: `SandboxAgent` with Unix-local `SandboxRunConfig`.
- Lab 04: SQL analyzer Agent with read-only function tools, local context, and
  structured output.
- Lab 05: Python voice pipeline plus a separate browser realtime implementation
  using ephemeral client secrets.
