"""
Audit trail — persist every extraction run as a reviewable artifact.

In payment integrity, output that cannot be audited cannot be defended:
each run records which note, which model and prompt version, live or
offline, and every finding (with evidence and code-validity flags) as
JSON under runs/<utc-timestamp>_<note-stem>/findings.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from .config import PROMPT_VERSION, have_api_key, model

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


def record(note_path, results: dict, runs_dir: Path = RUNS_DIR) -> Path:
    """Write one run artifact. `results` maps era name -> findings list."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    run_dir = runs_dir / f"{stamp}_{Path(note_path).stem}"
    run_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "note": str(note_path),
        "recorded_at_utc": stamp,
        "mode": "live" if have_api_key() else "offline-simulation",
        "model": model(),
        "prompt_version": PROMPT_VERSION,
        "findings": results,
    }
    out = run_dir / "findings.json"
    out.write_text(json.dumps(payload, indent=2))
    return run_dir
