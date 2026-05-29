# Lab 03: SandboxAgent Capability Sampler

## Goal

Show the main SandboxAgent capabilities before you use SandboxAgents for
larger project work.

## What You Build

A tiny repo and a SandboxAgent workflow that:

- Reads `AGENTS.md`
- Inspects files
- Runs tests
- Fixes a small bug
- Uses one skill
- Writes durable memory
- Resumes after a pause

## SandboxAgents Concepts

- Workspace-native execution
- `AGENTS.md`
- Filesystem capability
- Shell capability
- Skills
- Memory
- Workspace persistence
- Resumable work
- UnixLocal `SandboxRunConfig`

## Reference Solution Scope

Create a deliberately small `buggy-calculator` project:

- `calculator.py`
- `tests/test_calculator.py`
- One failing edge case
- One skill: `debug-failing-tests`
- One memory note about the project convention

## Checkpoint

You can explain the difference between:

- SDK session memory: conversation state
- Sandbox memory: durable workspace knowledge

You can also identify where the sandbox runtime is configured:

`RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(), ...))`
