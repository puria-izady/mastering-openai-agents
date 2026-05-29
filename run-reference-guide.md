# Reference Runner Guide

Each lab reference has a `run_reference.py` script for interactive use. Tests
verify the code; runner scripts let you experience the lab.

Set your OpenAI API key before running SDK labs:

```bash
export OPENAI_API_KEY="sk-..."
```

## Lab 00

```bash
cd mastering-openai-agents/lab-00-codex-workflow/reference-solution
uv run python run_reference.py README.md
```

## Lab 01

```bash
cd mastering-openai-agents/lab-01-agents-sdk-sampler/reference-solution
uv run python run_reference.py first-agent
uv run python run_reference.py structured
uv run python run_reference.py tool
uv run python run_reference.py guardrail
uv run python run_reference.py session
```

## Lab 02

```bash
cd mastering-openai-agents/lab-02-handoffs-patterns/reference-solution
uv run python run_reference.py handoff
uv run python run_reference.py tools
```

## Lab 03

```bash
cd mastering-openai-agents/lab-03-sandboxagent-sampler/reference-solution
uv run python run_reference.py
```

This runs the SandboxAgent through UnixLocal `SandboxRunConfig` and streams
progress events, including model text, tool calls, and tool outputs.

To run without streaming progress:

```bash
uv run python run_reference.py --no-stream
```

## Lab 04

```bash
cd mastering-openai-agents/lab-04-sql-analyzer/reference-solution
uv run python run_reference.py
```

Use the SQL Analyzer README for CLI options and custom questions.

## Lab 05

Python voice pipeline:

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution
uv run python run_reference.py --seconds 1
```

Without `OPENAI_API_KEY`, the voice demo skips cleanly. With a key, it runs a
static `AudioInput` through the SDK `VoicePipeline` and prints lifecycle/audio
stream summaries.

True browser realtime agent:

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution/realtime-browser
npm install
npm test
npm run typecheck
npm run build
export OPENAI_API_KEY="sk-..."
npm run server
```

In another terminal:

```bash
cd mastering-openai-agents/lab-05-realtime-voice-agent/reference-solution/realtime-browser
npm run dev
```

Open the HTTPS Vite URL and start the realtime session in the browser.
