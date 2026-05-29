# Prompt 2: Safety

Add a conservative read-only SQL safety layer.

Requirements:

- Allow SELECT and WITH queries.
- Reject INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, REPLACE, VACUUM, ATTACH,
  DETACH, PRAGMA, and semicolons.
- Ignore unsafe words inside string literals and comments.
- Add a SQLite authorizer for execution-time write protection.
- Add focused tests for accepted and rejected SQL.

Run the tests and summarize the behavior.

