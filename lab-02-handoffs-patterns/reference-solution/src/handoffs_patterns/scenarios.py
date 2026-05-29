from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    id: str
    prompt: str
    expected_specialist: str


SCENARIOS = [
    Scenario("billing", "Why was invoice INV-1002 higher this month?", "Billing specialist"),
    Scenario("technical", "The dashboard export button fails with a 500 error.", "Technical specialist"),
    Scenario("mixed", "My invoice is wrong and the export is broken.", "Support manager"),
]

