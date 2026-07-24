"""Audit-trail artifacts are written and complete."""

import json

from src import audit


def test_record_writes_complete_artifact(tmp_path):
    findings = {"past": [{"name": "Type 2 diabetes mellitus", "icd10": "E11.9"}]}
    run_dir = audit.record("data/notes/note1.txt", findings, runs_dir=tmp_path)

    payload = json.loads((run_dir / "findings.json").read_text())
    assert payload["note"] == "data/notes/note1.txt"
    assert payload["mode"] in ("live", "offline-simulation")
    assert payload["model"] and payload["prompt_version"]
    assert payload["findings"] == findings
