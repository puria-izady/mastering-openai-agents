# Verification Checklist

## Setup

- [ ] Created and activated a Python virtual environment
- [ ] Installed dependencies with `pip install -e ".[dev]"`
- [ ] Copied `.env.example` to `.env`
- [ ] Added `OPENAI_API_KEY`
- [ ] Seeded the database with `python -m sql_analyzer.seed`

## Local Verification

- [ ] Ran `pytest -q`
- [ ] Confirmed SQL safety tests pass
- [ ] Confirmed schema inspection tests pass
- [ ] Confirmed tool implementation tests pass

## Agent Verification

- [ ] Ran `sql-analyzer "Which products generated the most revenue?"`
- [ ] Saw SQL in the response
- [ ] Saw rows in the response
- [ ] Saw a business explanation
- [ ] Opened the traces dashboard and found the run
- [ ] Identified each tool call in the trace

## Reflection

- [ ] Wrote down the best Codex prompt you used
- [ ] Wrote down one prompt that was too broad
- [ ] Identified one deterministic safety rule
- [ ] Identified one thing the model should decide
- [ ] Added one extension idea

