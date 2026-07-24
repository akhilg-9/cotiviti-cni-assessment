# Sample data

- `note1.txt`, `note2.txt` — **synthetic** clinical notes (no real PHI), used as
  inputs to the proof of concept.
- `../test_cases.csv` — a small **labeled gold set**: the conditions, ICD-10
  codes, and expected statuses a correct system should extract from each note.
  Used by `src/evaluation.py` to score the rule-based vs. LLM passes.

These stand in for the kind of unstructured clinical documentation Cotiviti
reviews for risk adjustment and payment integrity.
