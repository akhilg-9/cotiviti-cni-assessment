"""ICD-10-CM validation against the official CMS FY2026 code set."""

from src import icd10


def test_valid_codes_pass():
    for code in ["E11.9", "I10", "N10", "I50.9", "A41.9"]:
        assert icd10.is_valid(code), code


def test_dotless_and_case_insensitive():
    assert icd10.is_valid("e119")
    assert icd10.is_valid("E119")


def test_invalid_codes_flagged():
    # R42 exists but has no subcodes — R42.0 was emitted live by the LLM once.
    for code in ["R42.0", "XX9.99", "", "not-a-code"]:
        assert not icd10.is_valid(code), code


def test_annotate_stamps_findings():
    findings = [{"icd10": "E11.9"}, {"icd10": "R42.0"}]
    icd10.annotate(findings)
    assert findings[0]["code_valid"] is True
    assert findings[1]["code_valid"] is False
