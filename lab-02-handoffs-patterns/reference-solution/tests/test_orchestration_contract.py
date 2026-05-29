from types import SimpleNamespace

from agents import Agent

from handoffs_patterns.agents_as_tools import build_manager, collect_tool_outputs
from handoffs_patterns.agents_handoff import build_specialists, build_triage_agent
from handoffs_patterns.run_config import build_run_config
from handoffs_patterns.scenarios import SCENARIOS


def test_handoff_triage_has_specialists() -> None:
    triage = build_triage_agent()
    assert isinstance(triage, Agent)
    assert len(triage.handoffs) == 2


def test_specialists_have_handoff_descriptions() -> None:
    billing, technical = build_specialists()
    assert billing.handoff_description
    assert technical.handoff_description


def test_agents_as_tools_manager_has_two_tools() -> None:
    manager = build_manager()
    assert isinstance(manager, Agent)
    assert len(manager.tools) == 2
    assert {tool.name for tool in manager.tools} == {
        "ask_billing_specialist",
        "ask_technical_specialist",
    }


def test_scenarios_cover_expected_routes() -> None:
    assert {scenario.id for scenario in SCENARIOS} == {"billing", "technical", "mixed"}


def test_run_config_is_visible_sdk_object() -> None:
    assert build_run_config().workflow_name == "lab-02-handoffs-patterns"


def test_collect_tool_outputs_reads_sdk_run_items() -> None:
    result = SimpleNamespace(
        new_items=[
            SimpleNamespace(type="message_output_item", output="ignore"),
            SimpleNamespace(type="tool_call_output_item", output="billing analysis"),
            SimpleNamespace(type="tool_call_output_item", output={"status": "ok"}),
        ]
    )
    assert collect_tool_outputs(result) == ["billing analysis", "{'status': 'ok'}"]
