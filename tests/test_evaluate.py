"""Scoring helpers in the evaluation harness."""

from src import evaluation as evaluate


def test_prf_perfect():
    p, r, f = evaluate._prf(tp=4, fp=0, fn=0)
    assert (p, r, f) == (1.0, 1.0, 1.0)


def test_prf_handles_empty():
    assert evaluate._prf(0, 0, 0) == (0.0, 0.0, 0.0)


def test_matches_on_icd10_and_name():
    gold = {"condition": "Atrial fibrillation", "icd10": "I48.91"}
    assert evaluate._matches(gold, {"name": "AFib", "icd10": "I48.91"})        # code match
    assert evaluate._matches(gold, {"name": "atrial fibrillation", "icd10": ""})  # name match
    assert not evaluate._matches(gold, {"name": "Diabetes", "icd10": "E11.9"})


def test_gold_set_loads():
    gold = evaluate._load_gold()
    assert "note1.txt" in gold and "note2.txt" in gold
    assert len(gold["note1.txt"]) == 6
