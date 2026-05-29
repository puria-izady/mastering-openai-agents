from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    primary_key: bool = False
    description: str = ""


class TableInfo(BaseModel):
    name: str
    description: str = ""
    columns: list[ColumnInfo]


class SchemaInfo(BaseModel):
    tables: list[TableInfo]


class ValidationResult(BaseModel):
    ok: bool
    reason: str
    normalized_preview: str = ""


class QueryResult(BaseModel):
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    truncated: bool = False


AnalysisValue = str | int | float | bool | None


class AnalysisAnswer(BaseModel):
    question: str = Field(description="The user's original business question.")
    sql: str = Field(description="The read-only SQL query used to answer.")
    columns: list[str] = Field(description="Columns returned by the query.")
    rows: list[list[AnalysisValue]] = Field(
        description="Compact result rows. Each row is an ordered list of values matching the columns array."
    )
    explanation: str = Field(description="Plain-English business explanation.")
    caveats: list[str] = Field(default_factory=list, description="Known limits or missing-data caveats.")
