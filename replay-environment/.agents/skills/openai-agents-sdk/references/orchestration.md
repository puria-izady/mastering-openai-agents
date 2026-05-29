# Orchestration

Teach both SDK orchestration choices explicitly.

Use function-call-safe names for generated tools. Handoffs are exposed as
function tools, so an agent named `Billing specialist` becomes a tool like
`transfer_to_billing_specialist`; the SDK may warn and sanitize invalid names.
Prefer SDK-facing agent/tool names with only letters, digits, and underscores,
or set explicit safe names such as `billing_specialist` and
`technical_specialist`.

Use handoffs when a specialist should own the current conversation after
routing:

```python
billing_agent = Agent(name="billing_specialist", instructions="Handle billing questions.")
technical_agent = Agent(name="technical_specialist", instructions="Handle technical questions.")

triage = Agent(
    name="support_triage",
    instructions="Route to the specialist that should own the reply.",
    handoffs=[billing_agent, technical_agent],
)
```

Use agents-as-tools when a manager should remain responsible for the final
answer and call specialists for focused analysis:

```python
manager = Agent(
    name="Support manager",
    instructions="Call specialists, then synthesize the final reply.",
    tools=[
        billing_agent.as_tool(
            tool_name="ask_billing_specialist",
            tool_description="Analyze billing questions.",
        )
    ],
)
```

Lab tests should verify the SDK contract: handoff managers have `handoffs`,
agents-as-tools managers have tool entries created by `Agent.as_tool`, and demos
use `Runner.run`.
