"""
Official ICD-10-CM code validation — a deterministic guard on the
probabilistic extractors.

data/icd10cm_codes_2026.txt is the code column of the CMS FY2026
"Code Descriptions in Tabular Order" release (74,719 valid codes,
https://www.cms.gov/medicare/coding-billing/icd-10-codes). CMS lists codes
without the dot (E119); clinical text uses the dotted form (E11.9), so
validation strips the dot before lookup.

An LLM can emit a well-formed code that does not exist (seen live: R42.0 —
R42 has no subcodes). `annotate` stamps every finding with `code_valid` so
downstream review can flag exactly those.
"""

import functools
from pathlib import Path

CODES_FILE = Path(__file__).resolve().parent.parent / "data" / "icd10cm_codes_2026.txt"


@functools.lru_cache(maxsize=1)
def _codes() -> frozenset:
    return frozenset(CODES_FILE.read_text().split())


def is_valid(code: str) -> bool:
    """True if `code` is in the official ICD-10-CM FY2026 code set."""
    return str(code).replace(".", "").strip().upper() in _codes()


def annotate(findings: list[dict]) -> list[dict]:
    """Stamp each finding with `code_valid` (in place); returns the list."""
    for f in findings:
        f["code_valid"] = is_valid(f.get("icd10", ""))
    return findings
