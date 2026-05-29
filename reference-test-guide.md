# Reference Test Guide

The reference suite has two layers.

## 1. Offline Contract Tests

These tests do not call OpenAI. They validate deterministic tools, fixtures,
schemas, SDK object construction, `RunConfig`, and the UnixLocal SandboxAgent
configuration.

```bash
for d in mastering-openai-agents/lab-{00,01,02,03,05}-*/reference-solution; do
  echo "== $d"
  (cd "$d" && uv run --with pytest pytest -q) || exit 1
done

cd mastering-openai-agents/lab-04-sql-analyzer/reference-solution
uv run --with pytest pytest -q
```

## 2. OpenAI API Smoke Tests

These tests call the OpenAI API for every SDK lab. Set `OPENAI_API_KEY` first.
Set `REQUIRE_OPENAI_API=1` so missing credentials fail instead of skipping.

```bash
export OPENAI_API_KEY="sk-..."
export REQUIRE_OPENAI_API=1

for d in mastering-openai-agents/lab-{01,02,03,05}-*/reference-solution; do
  echo "== $d"
  (cd "$d" && uv run --with pytest pytest -q tests/test_openai_integration.py) || exit 1
done

cd mastering-openai-agents/lab-04-sql-analyzer/reference-solution
uv run --with pytest pytest -q
```

Lab 04 includes an API-backed test in
`lab-04-sql-analyzer/reference-solution`; it skips only when `OPENAI_API_KEY`
is absent.

## What This Proves

- Offline tests prove the references are structurally correct and deterministic
  logic is reliable.
- OpenAI API smoke tests prove each SDK lab actually reaches OpenAI through
  `Runner.run(...)`.
- Lab 03 proves the SandboxAgent path reaches OpenAI while using UnixLocal
  `SandboxRunConfig`.
