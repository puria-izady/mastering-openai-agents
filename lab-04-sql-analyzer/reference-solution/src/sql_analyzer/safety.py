from __future__ import annotations

import re
import sqlite3

from .schemas import ValidationResult


MUTATION_TOKENS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "replace",
    "truncate",
    "vacuum",
    "attach",
    "detach",
    "pragma",
    "reindex",
}

DENIED_SQLITE_ACTIONS = {
    sqlite3.SQLITE_INSERT,
    sqlite3.SQLITE_UPDATE,
    sqlite3.SQLITE_DELETE,
    sqlite3.SQLITE_ALTER_TABLE,
    sqlite3.SQLITE_DROP_TABLE,
    sqlite3.SQLITE_DROP_INDEX,
    sqlite3.SQLITE_DROP_TRIGGER,
    sqlite3.SQLITE_DROP_VIEW,
    sqlite3.SQLITE_CREATE_TABLE,
    sqlite3.SQLITE_CREATE_INDEX,
    sqlite3.SQLITE_CREATE_TRIGGER,
    sqlite3.SQLITE_CREATE_VIEW,
    sqlite3.SQLITE_ATTACH,
    sqlite3.SQLITE_DETACH,
    sqlite3.SQLITE_PRAGMA,
}


def _strip_comments_and_strings(sql: str) -> str:
    output: list[str] = []
    i = 0
    in_single = False
    in_double = False
    in_line_comment = False
    in_block_comment = False

    while i < len(sql):
        char = sql[i]
        nxt = sql[i + 1] if i + 1 < len(sql) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                output.append(" ")
            i += 1
            continue

        if in_block_comment:
            if char == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue

        if in_single:
            if char == "'" and nxt == "'":
                i += 2
                continue
            if char == "'":
                in_single = False
            output.append(" ")
            i += 1
            continue

        if in_double:
            if char == '"':
                in_double = False
            output.append(" ")
            i += 1
            continue

        if char == "-" and nxt == "-":
            in_line_comment = True
            i += 2
            continue

        if char == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue

        if char == "'":
            in_single = True
            output.append(" ")
            i += 1
            continue

        if char == '"':
            in_double = True
            output.append(" ")
            i += 1
            continue

        output.append(char)
        i += 1

    return "".join(output)


def _tokens(sql: str) -> list[str]:
    scrubbed = _strip_comments_and_strings(sql).lower()
    return re.findall(r"[a-z_][a-z0-9_]*|;", scrubbed)


def validate_readonly_sql(sql: str) -> ValidationResult:
    stripped = sql.strip()
    if not stripped:
        return ValidationResult(ok=False, reason="SQL is empty.")

    tokens = _tokens(stripped)
    if not tokens:
        return ValidationResult(ok=False, reason="SQL has no executable tokens.")

    if ";" in tokens:
        return ValidationResult(ok=False, reason="Semicolons are not allowed in this lab.")

    first = tokens[0]
    if first not in {"select", "with"}:
        return ValidationResult(ok=False, reason="Only SELECT or WITH queries are allowed.")

    found_mutations = sorted(set(tokens).intersection(MUTATION_TOKENS))
    if found_mutations:
        return ValidationResult(
            ok=False,
            reason=f"Read-only validation rejected token(s): {', '.join(found_mutations)}.",
        )

    preview = re.sub(r"\s+", " ", stripped)[:160]
    return ValidationResult(ok=True, reason="SQL is read-only by static validation.", normalized_preview=preview)


def readonly_authorizer(action: int, arg1: str | None, arg2: str | None, db_name: str | None, trigger: str | None) -> int:
    if action in DENIED_SQLITE_ACTIONS:
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK

