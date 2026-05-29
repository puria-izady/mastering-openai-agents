# Resumption Worksheet

1. Start a run and ask the SandboxAgent to inspect the repo and run tests.
2. Stop after it explains the failing test.
3. Resume and ask it to implement the smallest fix.
4. Verify that the workspace still contains the prior analysis.
5. Close the session and inspect generated memory files.

Generated sandbox memory normally lives under `memories/` in the active sandbox
workspace. Inspect:

```bash
find <sandbox-root>/memories -maxdepth 2 -type f
cat <sandbox-root>/memories/MEMORY.md
cat <sandbox-root>/memories/memory_summary.md
```

Temporary UnixLocal sandbox workspaces may be deleted after cleanup. The stable
seeded course artifact is the local `memories/` folder. Runnable demos also
export the final sandbox workspace into `artifacts/` before deleting the
temporary UnixLocal workspace, so generated memories remain inspectable after
the process exits.
