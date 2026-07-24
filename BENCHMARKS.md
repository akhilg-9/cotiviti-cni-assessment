# Benchmarks

Each era is scored on the **same** labeled gold set (`data/test_cases.csv`,
11 conditions across 2 synthetic notes) by `src/evaluation.py`. Reproduce with:

```bash
cni eval
```

The gold set has a history worth telling: it began with 9 dictionary-curated
conditions, and the live LLM kept surfacing two findings that are verbatim in
the notes — lower-extremity edema ("Lower-extremity edema noted") and fatigue
("two weeks of worsening fatigue") — which the original labels omitted. The
model audited its own gold set; both findings are now labeled (v2, 11
conditions).

## Detection + status accuracy

Measured on `claude-haiku-4-5` (live, temperature 0) against gold v2:

| Era | TP | FP | FN | Precision | Recall | F1 | Status acc. |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Past** — rule-based | 9 | 0 | 2 | 1.00 | **0.82** | 0.90 | **89%** |
| **Present** — LLM (live Claude) | 11 | 0 | 0 | 1.00 | **1.00** | 1.00 | **100%** ✱ |

✱ Typical live run. LLM sampling still varies by at most one finding or one
status judgment between runs (e.g. recall 0.91, status 91%) even at
temperature 0; the rule-based row is deterministic and never changes. Offline
mode reuses the rule-based pass for the Present row (clearly labelled), so
offline rows match the Past row by construction.

## What the numbers say

- **Detection**: the rule-based pass finds only its 9 dictionary terms and
  misses edema and fatigue outright — recall 0.82 even on *synthetic* notes.
  The LLM finds all 11 with zero false positives. On uncurated real notes the
  gap widens dramatically (see below).
- **Status accuracy** separates the eras just as sharply. The note says
  *"Hypertension is suspected but not yet confirmed."* The rule-based negation
  heuristic only scans **backward** from the matched term, so it never sees the
  trailing "suspected" and labels hypertension **active** (wrong). The LLM
  reads the whole sentence and labels it **uncertain** (correct) → 89% → 100%.

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

## Code validity at scale (no labels required)

Because the official CMS ICD-10-CM table is itself ground truth, code validity
scales to any number of notes with zero hand-labeling. Across all audited runs
on real notes (`cni validity`, computed from the `runs/` artifacts):

| Era | Codes valid | Rate |
|---|--:|--:|
| Past — rules | 7/7 | 100% (curated dictionary) |
| Present — LLM | 90/92 | **97.8%** |
| Future — vision | 105/114 | **92.1%** |

The flagged codes tell two stories. Some simply don't exist (R61.9, R21.9 —
parents with no subcodes). More interesting: **M54.5, D59.1, and C91.1 were
valid in earlier ICD-10-CM years and have since been subdivided** — the model
emits codes from its training-data era, and validation against the *current*
fiscal-year table catches that drift. In payment integrity, an outdated code
is a denial; a deterministic, updatable code table is the guard.

## Limits of this benchmark

- 2 notes / 11 conditions — a demonstrator, not a validation study.
- Synthetic notes; real charts are messier (abbreviations, misspellings, scans).
- The gold set is authored by the same person who wrote the notes.

See [`WHAT_BROKE.md`](WHAT_BROKE.md) for the failure modes behind these choices.
