# Tools, Guardrails, And Sessions

Use `@function_tool` to expose deterministic local capabilities to an agent.
Tool functions are normal Python functions and should contain the local,
testable boundary: database reads, retrieval, fixture lookup, policy loading,
or simulated writes.

Use Pydantic `output_type` when the lab teaches structured output. Tests should
validate the Pydantic models locally without requiring model calls.

Use `input_guardrail` or `output_guardrail` when the lab teaches safety or
domain boundaries. Keep deterministic helper logic separately testable.

Use `SQLiteSession` or another SDK session type when the lab teaches memory.
This is conversation history memory, separate from SandboxAgent workspace or
sandbox memory.

Reference pattern:

```python
from agents import Agent, SQLiteSession, function_tool


@function_tool
def lookup_order(order_id: str) -> dict:
    """Return an order fixture by ID."""
    ...


agent = Agent(
    name="Support assistant",
    instructions="Use lookup_order before answering order questions.",
    tools=[lookup_order],
)

session = SQLiteSession("student-1", db_path="sessions.db")
```
