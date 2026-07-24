"""The terminology reference is well-formed."""

from src.codes import CONDITIONS, NEGATION_CUES


def test_every_condition_is_complete():
    for name, meta in CONDITIONS.items():
        assert meta["icd10"], f"{name} missing ICD-10"
        assert meta["hcc"], f"{name} missing HCC"
        assert meta["synonyms"], f"{name} has no synonyms"
        assert all(s == s.lower() for s in meta["synonyms"]), f"{name} synonyms must be lowercase"


def test_negation_cues_present():
    assert "denies" in NEGATION_CUES
    assert "suspected" in NEGATION_CUES
