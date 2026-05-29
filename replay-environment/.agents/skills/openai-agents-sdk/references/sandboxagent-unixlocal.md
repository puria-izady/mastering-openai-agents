# SandboxAgent And UnixLocal

Use `SandboxAgent` when the agent needs a workspace with files, shell commands,
skills, artifacts, memory, or resumable sandbox state.

The course default is Unix-local sandbox execution:

```python
from agents import RunConfig
from agents.sandbox import Manifest, SandboxAgent
from agents.run_config import SandboxRunConfig
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient


agent = SandboxAgent(
    name="Sandbox engineer",
    instructions="Inspect files, run tests, edit, and summarize verification.",
    default_manifest=manifest,
)

run_config = RunConfig(
    workflow_name="lab-03-sandboxagent-unix-local",
    sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(), manifest=manifest),
)
```

Keep `SandboxAgent` defaults on the agent and per-run sandbox client/session
choices in `RunConfig(... sandbox=SandboxRunConfig(...))`.

Do not use SandboxAgent for every lab by default. Use normal `Agent` when the
teaching target is tools, structured output, handoffs, guardrails, sessions, or
business workflow orchestration without workspace-native execution.
