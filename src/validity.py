"""
Code-validity metrics, computed from the audit trail.

Reads every runs/<run>/findings.json and reports, per era, how many emitted
ICD-10 codes exist in the official CMS ICD-10-CM code set. No hand labeling
required — the official table is the ground truth, so this metric scales to
any number of notes.

    python -m src.validity      (or: cni validity)
"""

import json
from pathlib import Path

from . import icd10
from .audit import RUNS_DIR


def collect(runs_dir: Path = RUNS_DIR) -> dict:
    """era -> {'total': n, 'valid': n, 'invalid': [(note, name, code), ...]}"""
    stats: dict = {}
    for artifact in sorted(runs_dir.glob("*/findings.json")):
        payload = json.loads(artifact.read_text())
        note = Path(payload["note"]).name
        for era, findings in payload["findings"].items():
            s = stats.setdefault(era, {"total": 0, "valid": 0, "invalid": []})
            for f in findings:
                code = f.get("icd10", "")
                s["total"] += 1
                if icd10.is_valid(code):
                    s["valid"] += 1
                else:
                    s["invalid"].append((note, f.get("name", "?"), code))
    return stats


def report(runs_dir: Path = RUNS_DIR) -> None:
    stats = collect(runs_dir)
    if not stats:
        print("No audit artifacts found under runs/ — run `cni run <note>` first.")
        return
    print("Code validity vs. official ICD-10-CM (from runs/ audit artifacts)")
    print("-" * 66)
    for era in ("past", "present", "future"):
        if era not in stats:
            continue
        s = stats[era]
        pct = 100 * s["valid"] / s["total"] if s["total"] else 0.0
        print(f"{era:8} {s['valid']:3}/{s['total']:<3} codes valid  ({pct:5.1f}%)")
    invalid = [x for era in stats.values() for x in era["invalid"]]
    if invalid:
        print("\nFlagged (code not in ICD-10-CM):")
        for note, name, code in invalid:
            print(f"  {code:8} {name}  [{note}]")


if __name__ == "__main__":
    report()
