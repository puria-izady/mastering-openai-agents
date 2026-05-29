# Human-In-The-Loop Approvals

Use SDK approval primitives for sensitive actions.

Mark a function tool with `needs_approval=True` when a model-chosen action must
pause before execution:

```python
from agents import Agent, Runner, function_tool


@function_tool(needs_approval=True)
def issue_refund(order_id: str, amount: float) -> str:
    """Simulate issuing a refund after human approval."""
    return f"Issued refund for {order_id}: {amount}"
```

Execution flow:

1. `Runner.run(...)` pauses with `result.interruptions`.
2. Convert to state with `result.to_state()`.
3. Resolve each approval with `state.approve(...)` or `state.reject(...)`.
4. Resume the original top-level agent with `Runner.run(agent, state, ...)`.

Keep audit logging outside model prose. The tool implementation owns the
side-effect boundary, and tests should verify the local tool/audit behavior
without requiring API calls.
