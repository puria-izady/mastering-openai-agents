import asyncio
import importlib.util
import os
from pathlib import Path

import pytest

from sql_analyzer.run_config import build_run_config
from sql_analyzer.schemas import AnalysisAnswer
from sql_analyzer.tools import AGENT_TOOLS
from sql_analyzer.agent import INSTRUCTIONS


def test_analysis_answer_contract_accepts_compact_result() -> None:
    answer = AnalysisAnswer(
        question="Which products generated the most revenue?",
        sql="SELECT name, revenue FROM product_revenue",
        columns=["name", "revenue"],
        rows=[["Analytics Pro", 1990.0]],
        explanation="Analytics Pro generated the most revenue.",
        caveats=["Sample data only."],
    )
    assert answer.rows[0][0] == "Analytics Pro"


def test_run_config_is_visible_sdk_object() -> None:
    run_config = build_run_config()
    assert run_config.workflow_name == "lab-04-sql-analyzer"
    assert run_config.trace_metadata["lab"] == "04"


def test_function_tool_schemas_hide_run_context() -> None:
    schemas = {tool.name: tool.params_json_schema for tool in AGENT_TOOLS}

    assert schemas["inspect_schema_tool"]["properties"] == {}
    assert "sql" in schemas["validate_sql_tool"]["properties"]
    assert "sql" in schemas["run_readonly_sql_tool"]["properties"]
    assert "wrapper" not in str(schemas)
    assert "context" not in str(schemas)


def test_agent_instructions_prevent_common_semicolon_failure() -> None:
    assert "no trailing semicolon" in INSTRUCTIONS
    assert "remove the semicolon" in INSTRUCTIONS
    assert "validate_sql_tool again" in INSTRUCTIONS


@pytest.mark.skipif(importlib.util.find_spec("agents") is None, reason="Requires openai-agents.")
def test_analysis_answer_schema_is_strict_sdk_compatible() -> None:
    from agents import AgentOutputSchema

    AgentOutputSchema(AnalysisAnswer)


@pytest.mark.skipif(
    importlib.util.find_spec("agents") is None or not os.getenv("OPENAI_API_KEY"),
    reason="Requires openai-agents and OPENAI_API_KEY.",
)
def test_agent_returns_structured_answer_when_api_key_is_available(tmp_path: Path) -> None:
    from sql_analyzer.app import ask
    from sql_analyzer.db import initialize_database

    db_path = tmp_path / "ecommerce.db"
    initialize_database(db_path)

    answer = asyncio.run(ask("Which products generated the most revenue?", db_path=db_path))
    assert isinstance(answer, AnalysisAnswer)
    assert answer.sql
    assert answer.rows
    assert answer.explanation


def test_agent_default_uses_luna_and_keeps_model_override(monkeypatch) -> None:
    from sql_analyzer.agent import build_agent

    monkeypatch.delenv("OPENAI_DEFAULT_MODEL", raising=False)
    assert build_agent().model == "gpt-6-luna"
    monkeypatch.setenv("OPENAI_DEFAULT_MODEL", "custom-model")
    assert build_agent().model == "custom-model"
    assert build_agent(model="explicit-model").model == "explicit-model"
