"""
Evaluation harness — scores the Past (rule-based) and Present (LLM) passes
against the labeled gold set in data/test_cases.csv.

    python -m src.evaluation       (or: cni eval)

Reports precision / recall / F1 on condition detection and status accuracy, so
the brittleness-vs-reasoning story is backed by numbers, not just side-by-side
panels. (Mirrors the test-cases + evaluation pattern from a typical agentic-AI
reference project.)
"""

import csv
import os

from . import llm_extract, rules_ner

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
NOTES = os.path.join(DATA, "notes")


def _load_gold():
    gold = {}
    with open(os.path.join(DATA, "test_cases.csv")) as f:
        for row in csv.DictReader(f):
            gold.setdefault(row["note_file"], []).append(row)
    return gold


def _matches(gold_row, pred):
    """A prediction matches a gold row if the ICD-10 code matches, or the
    condition names overlap (handles LLM phrasing differences)."""
    if gold_row["icd10"].split(".")[0] == str(pred.get("icd10", "")).split(".")[0]:
        return True
    g = gold_row["condition"].lower()
    p = str(pred.get("name", "")).lower()
    return g in p or p in g


def _score(note_file, gold_rows, preds):
    tp = fp = 0
    status_correct = 0
    matched_gold = set()
    for pred in preds:
        hit = next((i for i, g in enumerate(gold_rows)
                    if i not in matched_gold and _matches(g, pred)), None)
        if hit is None:
            fp += 1
        else:
            tp += 1
            matched_gold.add(hit)
            # status accuracy: treat negated/uncertain families loosely
            exp = gold_rows[hit]["expected_status"]
            got = str(pred.get("status", "")).lower()
            if exp in got or got in exp or (exp == "uncertain" and "negat" in got):
                status_correct += 1
    fn = len(gold_rows) - len(matched_gold)
    return tp, fp, fn, status_correct


def _prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


def evaluate():
    gold = _load_gold()
    methods = {
        "Past  (rule-based)": rules_ner.extract,
        "Present (LLM)": llm_extract.extract,
    }
    print("=" * 70)
    print("Evaluation vs. labeled gold set (data/test_cases.csv)")
    print("=" * 70)
    print(f"{'METHOD':22} {'TP':>3} {'FP':>3} {'FN':>3} {'PREC':>6} {'REC':>6} {'F1':>6} {'STATUS':>7}")
    print("-" * 70)

    for name, fn_extract in methods.items():
        TP = FP = FN = SC = 0
        for note_file, rows in gold.items():
            with open(os.path.join(NOTES, note_file)) as fh:
                preds = fn_extract(fh.read())
            tp, fp, fnc, sc = _score(note_file, rows, preds)
            TP += tp; FP += fp; FN += fnc; SC += sc
        p, r, f = _prf(TP, FP, FN)
        status_acc = SC / TP if TP else 0.0
        print(f"{name:22} {TP:3d} {FP:3d} {FN:3d} {p:6.2f} {r:6.2f} {f:6.2f} {status_acc:6.0%}")

    print("-" * 70)
    print("STATUS = share of detected conditions with the correct active/negated/")
    print("uncertain label. Note the rule-based pass mislabels 'suspected'")
    print("hypertension as active; the LLM resolves it from context.\n")


if __name__ == "__main__":
    evaluate()
