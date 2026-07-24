"""
"PAST" — the classic clinical-NLP approach.

Dictionary + regex named-entity recognition with simple negation detection.
This is roughly how clinical concept extraction worked before LLMs: a curated
term list, string matching, and a hand-written negation heuristic (a tiny
cousin of the well-known NegEx algorithm).

It is fast, fully offline, and deterministic — but brittle: it only finds terms
it was told about, and its negation logic is shallow. That contrast is the whole
point of the demo.
"""

import re

from .codes import CONDITIONS, NEGATION_CUES


def _is_negated(text_lower: str, span_start: int) -> bool:
    """Look in a small window before the match for a negation/uncertainty cue."""
    window = text_lower[max(0, span_start - 45):span_start]
    return any(cue in window for cue in NEGATION_CUES)


def extract(note_text: str) -> list[dict]:
    """Return a list of condition findings using rule-based matching."""
    text_lower = note_text.lower()
    findings = {}  # canonical name -> finding (dedupe; keep first/active hit)

    for canonical, meta in CONDITIONS.items():
        for syn in meta["synonyms"]:
            for m in re.finditer(r"\b" + re.escape(syn) + r"\b", text_lower):
                negated = _is_negated(text_lower, m.start())
                status = "negated/uncertain" if negated else "active"
                # Prefer an active hit over a negated one if the term appears twice.
                existing = findings.get(canonical)
                if existing and existing["status"] == "active":
                    continue
                findings[canonical] = {
                    "name": canonical,
                    "icd10": meta["icd10"],
                    "hcc": meta["hcc"],
                    "status": status,
                    "evidence": note_text[m.start():m.end()],
                    "confidence": 0.6,  # rule-based has no real confidence; flat heuristic
                    "method": "rule-based",
                }
                break  # first synonym match is enough for this condition

    return list(findings.values())
