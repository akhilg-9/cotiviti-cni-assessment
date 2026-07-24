# Benchmarks

Each era is scored on the **same** labeled gold set (`data/test_cases.csv`,
9 conditions across 2 synthetic notes) by `src/evaluation.py`. Reproduce with:

```bash
cni eval
```

## Detection + status accuracy

Measured on `claude-haiku-4-5` (live) and offline:

| Era | TP | FP | FN | Precision | Recall | F1 | Status acc. |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Past** — rule-based | 9 | 0 | 0 | 1.00 | 1.00 | 1.00 | **89%** |
| **Present** — LLM (offline sim.) | 9 | 0 | 0 | 1.00 | 1.00 | 1.00 | 89% |
| **Present** — LLM (live Claude) | 9 | 1 | 0 | 0.90 | 1.00 | 0.95 | **100%** ✱ |

✱ Live: the LLM resolves the one status case the rule-based pass gets wrong
(→ 100% status accuracy). Its single "false positive" is **lower-extremity
edema (R60.0)** — a real finding in note1 ("Lower-extremity edema noted") that
isn't in the curated gold set. Against this small gold set it scores as an FP,
but it's clinically correct: the LLM generalises *beyond* the dictionary.
Offline mode reuses the rule-based pass for the Present row (clearly labelled),
so the two offline rows match by construction. LLM outputs can vary slightly
run-to-run even at temperature 0.

## What the numbers say

- **Detection** recall ties on this curated set — every gold condition is in the
  rule-based dictionary, so both passes find all 9. But the live LLM *also*
  surfaced lower-extremity edema, which the dictionary cannot. On *uncurated*
  real notes the rule-based recall would fall (it only finds terms it was told
  about); the LLM generalises beyond the dictionary — visible here as that one
  "extra" finding.
- **Status accuracy** is where the eras separate. The note says *"Hypertension
  is suspected but not yet confirmed."* The rule-based negation heuristic only
  scans **backward** from the matched term, so it never sees the trailing
  "suspected" and labels hypertension **active** (wrong). The LLM reads the
  whole sentence and labels it **uncertain** (correct) → 89% → 100%.

## Why this matters for Cotiviti

In risk adjustment and payment integrity, *status* is the difference between a
defensible code and an incorrect one. A condition that is "suspected" or
"ruled out" must not be coded as active. The benchmark shows the rule-based
baseline failing exactly there, and the LLM fixing it — with evidence spans and
confidence attached for auditability.

## Real-world notes (unlabeled spot check)

The synthetic gold set favors the dictionary by construction, so we also ran
the pipeline live on real, publicly available de-identified notes
(`data/notes/real_pdfs/`, see its README for sources). No gold labels — counts
only, but the gap is stark:

| Note | Past (rules) | Present (LLM) | Future (vision, paginated scan) |
|---|--:|--:|--:|
| UHN discharge summary (pyelonephritis) | 2 | 9 | 10 |
| UCF comprehensive H&P (RA workup) | ~2 | ~25 | 12+ |

- The rule-based pass finds **only** dictionary terms (T2DM, HTN) and misses
  the actual discharge diagnosis (pyelonephritis N10), AKI, sepsis, BPH, and
  more — all captured by the LLM/LMM passes with correct active/uncertain/
  historical statuses (e.g. Sjögren's flagged *uncertain*, family history
  flagged *historical* in the UCF H&P).
- Multi-page scans initially crippled the vision pass (the renderer clipped
  long notes to one page); after paginating the synthetic scan, vision matched
  the text LLM on the UHN note and additionally surfaced E. coli bacteremia.
- Caveat: without gold labels these are detection counts, not precision — and
  some LLM/LMM ICD-10 codes are imprecise (e.g. "depressed mood" → R40.1,
  which is actually stupor). Nonexistent codes are now caught deterministically:
  every LLM/vision finding is checked against the official CMS FY2026
  ICD-10-CM code set (`src/icd10.py`, 74,719 codes) and flagged in the output
  (seen live: R61.9 / R21.9 emitted for parent codes that have no subcodes).
  Codes that exist but are clinically wrong still require the human-in-the-loop
  review the report recommends. Every run also writes an auditable artifact to
  `runs/` (see `runs/sample_run/`).

## Limits of this benchmark

- 2 notes / 9 conditions — a demonstrator, not a validation study.
- Synthetic notes; real charts are messier (abbreviations, misspellings, scans).
- The gold set is authored by the same person who wrote the notes.

See [`WHAT_BROKE.md`](WHAT_BROKE.md) for the failure modes behind these choices.
