"""
"PRESENT" — LLM-based structured extraction with Claude.

Sends the free-text note to Claude and asks for a structured list of clinically
codeable conditions: name, ICD-10 code, status (active / historical / negated /
uncertain), the evidence span it relied on, and a calibrated confidence. Unlike
the rule-based matcher, the model can normalise abbreviations, reason about
negation and uncertainty in context, and surface conditions that weren't in any
hand-built dictionary.

The prompt lives in prompts/v1.yaml; the JSON schema lives in src/models.py.
If no ANTHROPIC_API_KEY is set, falls back to an offline approximation so the
demo still runs end-to-end (clearly labelled as a simulation).
"""

import json

from . import icd10, rules_ner
from .config import get_client, model, prompts
from .models import EXTRACTION_SCHEMA, validate_conditions

# Exposed for the vision (Future/LMM) path to reuse the same contract.
SCHEMA = EXTRACTION_SCHEMA
PROMPT = prompts()["extraction"]["system"]


def _offline(note_text: str):
    """Deterministic fallback when no API key is present: reuse the rule-based
    pass but relabel it so the UI is honest about what produced it."""
    out = []
    for f in rules_ner.extract(note_text):
        out.append({
            "name": f["name"],
            "icd10": f["icd10"],
            "status": "negated" if "negat" in f["status"] else "active",
            "evidence": f["evidence"],
            "confidence": f["confidence"],
            "method": "llm (offline simulation)",
        })
    return out


def extract(note_text: str):
    client = get_client()
    if client is None:
        return _offline(note_text)

    msg = client.messages.create(
        model=model(),
        max_tokens=4000,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": PROMPT.format(note=note_text)}],
    )
    text = next(b.text for b in msg.content if b.type == "text")
    data = json.loads(text)
    conditions = validate_conditions(data["conditions"])
    return icd10.annotate([{**c, "method": "llm (Claude)"} for c in conditions])
