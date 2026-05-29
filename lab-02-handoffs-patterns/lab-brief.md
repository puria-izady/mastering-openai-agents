# Lab 02: Handoffs and Agents-as-Tools

## Goal

Teach the central orchestration decision: when a specialist should own the reply
with a handoff, and when a specialist should be called as a tool.

## What You Build

A customer-support triage app with:

- Triage manager
- Billing specialist
- Technical specialist
- Handoff version
- Agents-as-tools version
- Trace comparison worksheet

## OpenAI Agents Concepts

- `handoffs`
- `handoff_description`
- `agent.as_tool(...)`
- Specialist ownership
- `result.last_agent`
- Trace inspection

## Reference Solution Scope

The same three business scenarios should be run through both designs:

- Billing question
- Technical troubleshooting question
- Mixed question that needs synthesis

## Checkpoint

You can explain:

- Handoff means the specialist owns the conversation.
- Agent-as-tool means the manager keeps ownership and uses the specialist as a
  callable capability.

