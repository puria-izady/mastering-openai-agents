# Course Lab Patterns From Labs 01-05

Use these notes when rebuilding or extending the course labs. They preserve
reference-level implementation decisions that are easy to lose during replay.

## Lab 01: Agents SDK Sampler

Teach the smallest direct SDK surfaces first:

- Define real `Agent` objects and execute them with `Runner.run(...)`.
- Pass a visible `RunConfig` into runnable examples. Include `workflow_name`
  and `trace_metadata` so you know where traces come from.
- For structured extraction, use a Pydantic `output_type` and test the model
  locally without API calls.
- For tools, use deterministic `@function_tool` functions. Print
  `final_output` and enough `new_items` detail to show tool calls/results.
- For guardrails, keep the local domain/policy logic separately testable and
  make API-backed allowed/blocked demos skip cleanly without `OPENAI_API_KEY`.
- For session memory, compare stateless runs with SDK `Session`-backed runs.
  This is conversation history memory, not SandboxAgent workspace memory.

## Lab 02: Handoffs And Agents As Tools

Teach both orchestration patterns explicitly:

- Handoffs: a triage agent uses `handoffs=[billing_agent, technical_agent]`
  when the specialist should own the conversation after routing.
- Agents as tools: a manager uses `specialist.as_tool(...)` when the manager
  should remain responsible for the final answer.
- Use safe SDK-facing names for agents and tools: lowercase letters, digits,
  and underscores. Handoff names become generated tools.
- Demo runners should print `final_output` and `result.last_agent.name`.
- Agents-as-tools demos should also show captured specialist tool outputs from
  SDK run items so you can compare specialist analysis with the manager's
  final synthesis.
- Tests should assert real SDK contracts: `handoffs` exist for the handoff
  manager, `Agent.as_tool(...)` outputs are in manager tools, and `Runner.run`
  receives `RunConfig`.

## Lab 03: SandboxAgent Sampler

Use `SandboxAgent` only when workspace-native execution is the teaching goal:
files, shell commands, skills, memory, artifacts, or resumable sandbox state.

Course defaults:

- Use UnixLocal with `RunConfig(sandbox=SandboxRunConfig(...))`.
- Manifest destination paths must be relative. Do not mount to absolute
  `/workspace`.
- Mount the tiny calculator workspace as `repo`.
- Prefer synthetic SDK `Dir` and `File` entries for tiny lab repos. This
  avoids `LocalDir` problems when the course project lives under macOS
  permission-restricted folders.
- Add a smoke test that calls `manifest.validated_entries()`.
- Create the agent with explicit capabilities needed by the lab:
  `Filesystem()`, `Shell()`, `Skills(...)`, and `Memory()`.
- Keep skills small and mounted with `Skills(...)`; do not manually mount a
  full `.agents` tree for this tiny lab.
- Stream demos with `Runner.run_streamed(...)` and print startup context,
  model text deltas, tool calls, tool arguments, tool outputs, and final output.
  Keep a `--no-stream` path that uses `Runner.run(...)`.

Sandbox memory guidance:

- `Memory()` generates and reads SDK-managed memory artifacts. Do not prompt
  the agent to patch `../memories/...`; sandbox file tools must stay inside the
  workspace root.
- Memory generation happens when the sandbox session closes. Inspect generated
  `memories/MEMORY.md` and `memories/memory_summary.md` in the active sandbox
  workspace before cleanup, or preserve a snapshot/session if later inspection
  is required.
- For this course lab, the memory exercise can be a worksheet plus seeded
  memory files and local tests for capability/configuration. Do not make a
  required two-run API-backed memory test unless the lab explicitly asks for it.

## Lab 04: SQL Analyzer Agent

Keep database work deterministic and local until the agent layer:

- Use a `src/` package layout with `sql_analyzer`.
- Generate `data/ecommerce.db` from a seed command. Do not hand-edit or depend
  on an opaque binary fixture.
- Seed deterministic ecommerce tables: `customers`, `products`, `orders`,
  `order_items`, and `refunds`.
- Keep local database helpers directly callable:
  `initialize_database`, `inspect_schema`, and read-only query execution.
- Add a conservative SQL safety layer before exposing tools:
  allow `SELECT` and `WITH`; reject writes/admin statements and semicolons;
  ignore unsafe words inside string literals and comments; use a SQLite
  authorizer for execution-time write protection.
- Expose tools with `@function_tool`:
  `inspect_schema_tool`, `validate_sql_tool`, and `run_readonly_sql_tool`.
- Database tools must receive
  `ctx: RunContextWrapper[SqlAnalyzerContext]` and read the DB dependency from
  `ctx.context`. Do not use environment mutation or module-level global DB
  state for tool execution.
- Keep implementation functions separately callable so tests run without an API
  key. Test that generated tool schemas do not expose the run-context argument.
- Type the agent as `Agent[SqlAnalyzerContext]`.
- Pass the DB dependency with `Runner.run(..., context=...)`.
- Keep `RunConfig` visible with `workflow_name` and `trace_metadata`.
- Use a strict structured output model such as `AnalysisAnswer`. Avoid
  `dict[str, Any]` in final output. Represent rows as
  `list[list[str | int | float | bool | None]]` ordered to match `columns`.
- Add a local test that constructs `AgentOutputSchema(AnalysisAnswer)` so
  strict schema issues are caught before model calls.
- The agent instructions should require schema inspection before SQL, SQL
  validation before execution, SQL without semicolons, semicolon repair by
  validating again, business-language explanation, and caveats.

## Lab 05: Voice And Realtime Agent

Keep Python voice and browser realtime as separate architectures:

- Python voice reuse should use SDK `VoicePipeline`,
  `VoicePipelineConfig`, `SingleAgentVoiceWorkflow`, callbacks, and static
  `AudioInput` objects.
- Browser speech-to-speech realtime should use the TypeScript
  `RealtimeAgent` and `RealtimeSession` path over WebRTC. Do not present
  Python `VoicePipeline` as the realtime browser solution.
- A trusted server must mint ephemeral realtime client secrets. Keep
  `OPENAI_API_KEY` server-side only; the browser receives only the ephemeral
  client secret.
- Use model `gpt-realtime-2` for the browser realtime app.
- Include an `OpenAI-Safety-Identifier` header on the server-side client-secret
  request.
- Use HTTPS or localhost for browser microphone access.

Python voice demo guidance:

- `--seconds` alone should use generated silence as static `AudioInput` and
  print that clearly. It must not imply microphone capture.
- Real microphone capture should require `--record`.
- Optional microphone support should document `uv sync --extra dev --extra mic`
  and `uv run --extra mic ...`; installing into a different environment can
  leave `sounddevice` unavailable to `uv run`.
- When `--record` is used, print captured transcription from
  `SingleAgentWorkflowCallbacks` so you can verify what STT heard.
- TTS output arrives as `voice_stream_event_audio` chunks. Count/print samples
  for verification, and play response audio by default for `--record` runs.
  Provide `--no-playback` for CI/classroom use.
- Disable sensitive audio payload tracing with
  `trace_include_sensitive_audio_data=False` while keeping workflow tracing and
  metadata enabled.

Realtime browser logging guidance:

- Configure input audio transcription explicitly so the UI can show
  `You said: ...`.
- Log useful transport events, not every `history_updated` event.
- Show completed user and assistant transcript events, response completion,
  audio start/stop, interruptions, and errors.
- Do not log assistant transcript deltas as final answers; use one completed
  assistant transcript per visible response.
- Do not also display SDK `agent_end` output as a duplicate assistant answer
  when the transport transcript already logged the answer.
- Suppress empty input transcription logs.
- Tune semantic VAD with low eagerness for this teaching app to reduce noisy or
  empty turns.
- If one answer appears twice in the UI, first debug event logging. The same
  model turn may surface through transcript, audio, and lifecycle events.

## Cross-Lab Replay Rules

- Keep lab prompt packs complete enough for replay. Do not require reading a
  finished `reference-solution/`.
- Record prompt steps and verification in `BUILD-LOG.md`.
- API-backed demos should skip cleanly without `OPENAI_API_KEY`.
- Local tests should verify deterministic helpers and SDK object contracts,
  not exact model prose.
- Prefer direct SDK objects over course-specific abstraction layers.
