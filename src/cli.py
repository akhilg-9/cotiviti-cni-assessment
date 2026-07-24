"""
Typer CLI for Clinical Note Intelligence.

    cni run [NOTE]     # Past -> Present -> Future on a clinical note
    cni eval           # score the passes against the labeled gold set

(`cni` is installed as a console script; equivalently `python -m src.cli`.)
Set ANTHROPIC_API_KEY for live Claude calls; otherwise runs offline-simulated.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import audit, llm_extract, rules_ner, scan, vision_extract
from .config import ROOT, have_api_key, model

app = typer.Typer(help="Clinical Note Intelligence — Past / Present / Future clinical NLP.",
                  add_completion=False)
console = Console()

NOTES_DIR = ROOT / "data" / "notes"


def _table(title: str, subtitle: str, findings) -> Table:
    t = Table(title=f"{title}\n[dim]{subtitle}[/dim]", title_justify="left", expand=True)
    t.add_column("Condition", style="bold")
    t.add_column("ICD-10")
    t.add_column("Status")
    t.add_column("Conf", justify="right")
    for f in findings:
        status_style = "red" if "negat" in f["status"] or "uncert" in f["status"] else "green"
        # code_valid is stamped by src/icd10.py on LLM/vision output; the
        # rule-based pass uses curated codes, so absence means "not checked".
        code = f["icd10"] if f.get("code_valid", True) else f"[red]{f['icd10']} ⚠ not in ICD-10-CM[/red]"
        t.add_row(f["name"], code, f"[{status_style}]{f['status']}[/{status_style}]",
                  f"{float(f['confidence']):.2f}")
    if not findings:
        t.add_row("(none)", "", "", "")
    return t


@app.command()
def run(note: Optional[Path] = typer.Argument(None, help="Note file; defaults to data/notes/note1.txt")):
    """Run Past -> Present -> Future extraction on a clinical note."""
    note_path = note or (NOTES_DIR / "note1.txt")
    text = Path(note_path).read_text()
    mode = f"LIVE ({model()})" if have_api_key() else "OFFLINE simulation (no ANTHROPIC_API_KEY)"
    console.rule(f"[bold]Clinical Note Intelligence[/bold]  ·  {mode}")
    console.print(f"[dim]note: {note_path}[/dim]\n")

    past = rules_ner.extract(text)
    present = llm_extract.extract(text)
    console.print(_table("PAST", "rule-based dictionary + negation", past))
    console.print(_table("PRESENT", "LLM structured extraction (Claude)", present))

    scan_path = NOTES_DIR / "scanned_note.png"
    scan_pages = scan.render_pages(text, str(scan_path))
    console.print(f"[dim](rendered synthetic scan -> {len(scan_pages)} page(s), {scan_pages[0]})[/dim]")
    future = vision_extract.extract(scan_pages, offline_text=text)
    console.print(_table("FUTURE / LMM", "multimodal vision on scanned image", future))

    run_dir = audit.record(note_path, {"past": past, "present": present, "future": future})
    console.print(f"[dim](audit artifact -> {run_dir}/findings.json)[/dim]")


@app.command("eval")
def eval_cmd():
    """Score the passes against the labeled gold set (data/test_cases.csv)."""
    from .evaluation import evaluate
    evaluate()


def main():  # entry-point used by `python -m src.cli`
    app()


if __name__ == "__main__":
    app()
