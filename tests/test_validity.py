"""Validity metrics aggregate correctly from audit artifacts."""

import json

from src import validity


def test_collect_counts_valid_and_invalid(tmp_path):
    run = tmp_path / "2026-07-24T000000Z_note1"
    run.mkdir()
    (run / "findings.json").write_text(json.dumps({
        "note": "data/notes/note1.txt",
        "findings": {
            "present": [
                {"name": "T2DM", "icd10": "E11.9"},
                {"name": "Night sweats", "icd10": "R61.9"},
            ]
        },
    }))
    stats = validity.collect(tmp_path)
    assert stats["present"]["total"] == 2
    assert stats["present"]["valid"] == 1
    assert stats["present"]["invalid"][0][2] == "R61.9"
