---
name: openai-agents-sdk
description: Use when building or reviewing course labs that teach the OpenAI Agents SDK, including Agent, Runner, tools, handoffs, sessions, guardrails, RunConfig, SandboxAgent, UnixLocal SandboxRunConfig, RunState approvals, tracing, and SDK-first testing patterns.
---

# OpenAI Agents SDK

Use this Skill for this course's SDK reference implementations. The goal is to
teach the real OpenAI Agents SDK, not a course-specific abstraction.

## Core Rules

- Build directly with SDK objects: `Agent`, `SandboxAgent`, `Runner`,
  `RunConfig`, tools, handoffs, sessions, guardrails, and `RunState`.
- Do not create custom framework wrappers around agent execution.
- Use helpers only when they return real SDK objects, for example
  `build_agent()` or `build_run_config()`.
- Keep deterministic code in tools, fixtures, evals, and tests.
- Use function-call-safe tool and handoff names: lowercase letters, digits, and
  underscores only. Avoid spaces or display punctuation in `Agent.name` values
  that become handoff tools, or provide explicit safe tool names.
- API-backed demos may require `OPENAI_API_KEY`, but local tests must still run
  without making model calls.

## Reference Map

Read the smallest reference needed for the current task:

- `references/core-sdk.md` for `Agent`, `Runner`, `RunConfig`, results, and
  tracing.
- `references/tools-guardrails-sessions.md` for function tools, guardrails, and
  sessions.
- `references/orchestration.md` for handoffs and agents-as-tools.
- `references/sandboxagent-unixlocal.md` for `SandboxAgent`,
  `SandboxRunConfig`, manifests, capabilities, and Unix-local execution.
- `references/hitl-approvals.md` for `needs_approval`, interruptions,
  `RunState`, approval, and rejection.
- `references/testing-patterns.md` for local tests, API-backed smoke tests, and
  evals.
- `references/course-lab-patterns.md` for reusable implementation knowledge
  preserved from Labs 01-05, including sampler, handoffs, SandboxAgent,
  SQL analyzer, and voice/realtime lab choices.

## Official Sources

- Skill-local official SDK checkout: `openai-agents-python`
- Public docs quickstart:
  `https://developers.openai.com/api/docs/guides/agents/quickstart`
- Public sandbox docs:
  `https://developers.openai.com/api/docs/guides/agents/sandboxes`

When public docs and the local SDK checkout differ, inspect the installed SDK
version and official examples before changing course references.
