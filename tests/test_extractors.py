"""Rule-based extractor behaviour (runs fully offline)."""

import os

from src import rules_ner

NOTES = os.path.join(os.path.dirname(__file__), "..", "data", "notes")


def _note(name):
    with open(os.path.join(NOTES, name)) as f:
        return f.read()


def test_finds_core_conditions_with_codes():
    findings = {f["name"]: f for f in rules_ner.extract(_note("note1.txt"))}
    assert "Type 2 diabetes mellitus" in findings
    assert findings["Type 2 diabetes mellitus"]["icd10"] == "E11.9"
    assert findings["Congestive heart failure"]["icd10"] == "I50.9"


def test_documents_rule_based_limitation():
    # The rule-based pass only looks BACKWARD for negation cues, so it mislabels
    # "hypertension ... suspected, not yet confirmed" as active. This test pins
    # that known limitation (the LLM pass resolves it from context).
    findings = {f["name"]: f for f in rules_ner.extract(_note("note1.txt"))}
    assert findings["Essential hypertension"]["status"] == "active"
