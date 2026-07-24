# What broke (and what it taught the design)

A short, honest log of failure modes hit while building this demonstrator, and
the design decisions each one forced.

## 1. Rule-based negation only looks backward

**Symptom.** *"Hypertension is suspected but not yet confirmed"* was coded as an
**active** diagnosis.

**Cause.** The `NegEx`-style heuristic scans a fixed window *before* the matched
term for cues like "no" / "denies". The uncertainty cue ("suspected") comes
*after* the term, so it's invisible to a backward-only scan.

**What it taught.** This isn't a bug to patch — it's the whole point. I kept the
limitation, pinned it in a test (`tests/test_extractors.py`), and made the
evaluation surface it as a status-accuracy gap. The contrast *is* the demo: a
shallow rule can't reason about sentence-level context; the LLM can.

## 2. Multimodal beats a brittle OCR stage

**Symptom.** A first sketch used a separate OCR engine (Tesseract) before the
NLP step — an extra binary dependency, an extra point of failure, and poor
results on a skewed scan.

**Fix.** Drop OCR entirely. A large *multimodal* model reads the scanned PNG
directly (`src/vision_extract.py`), collapsing OCR → NLP into one step and
removing the dependency. This is also the more honest "Future" story.

## 3. The demo had to run with no API key

**Symptom.** A reviewer without an Anthropic key (or offline) would see nothing.

**Fix.** Every Claude-backed step degrades to a clearly-labelled offline
simulation (`have_api_key()` gate in `src/config.py`). The pipeline, the CLI,
the notebook, and the tests all run end-to-end with zero credentials; live mode
is strictly an upgrade.

## 4. Prompts buried in code are hard to iterate

**Symptom.** Early on the extraction prompt lived inside `llm_extract.py`, so
"tune the prompt" meant editing source and the contract could drift from the
schema.

**Fix.** Externalise prompts to `prompts/v1.yaml` and the schema to
`src/models.py`. Bumping the prompt file is now the unit of change — the same
pattern the eval suite gates on in the reference project.

## 5. PHI is a non-starter

**Symptom.** Real clinical notes can't go in a public repo.

**Fix.** All notes are synthetic and explicitly marked. Nothing here is real
patient data, and the README/report repeat that the prototype is not for
clinical use.
