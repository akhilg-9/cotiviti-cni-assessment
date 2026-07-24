# Structure comparison: this repo vs. the reference project

Reference: **akhilg-9 / agentic-devops-triage** — a three-tier autonomy-ladder
agentic system (router → planner → ReAct), with a `src/` layout, externalized
YAML prompts, a CI workflow, an evaluation harness, and `BENCHMARKS.md` /
`WHAT_BROKE.md` narrative docs.

This Clinical NLP submission mirrors that project's **engineering conventions**,
adapted to a different topic (Topic 1, Clinical NLP) and provider (Claude, not
OpenAI). Below is exactly what was adopted, adapted, and left out.

## Adopted (same conventions)

| Convention in agentic-devops-triage | How this repo does it |
|---|---|
| `src/` flat-module package + `pyproject.toml` (`packages.find`, console script) | `src/` with `cni = "src.cli:app"` |
| **Typer** CLI + **rich** output | `src/cli.py` — `cni run` / `cni eval` |
| `app.py` + `demo.py` at the root | Streamlit `app.py` + scripted `demo.py` |
| Externalized **versioned prompts** (`prompts/v1.yaml`) | `prompts/v1.yaml` — model + extraction prompt |
| `config.py` loads `.env` + prompt YAML | `src/config.py` (python-dotenv + pyyaml) |
| **pydantic** schema | `src/models.py` — `Condition` + JSON schema |
| `data/` docs + labeled test CSV | `data/notes/*.txt` + `data/test_cases.csv` |
| **Evaluation harness** + `BENCHMARKS.md` | `src/evaluation.py` + `BENCHMARKS.md` |
| `WHAT_BROKE.md` failure log | `WHAT_BROKE.md` |
| `.env.example`, `.github/workflows/ci.yml`, badge README | all present |
| `tests/` suite | `tests/` (11 tests, offline) |
| Notebooks | `notebooks/clinical_note_intelligence.ipynb` |

## Adapted (same idea, different shape)

| Reference | This repo | Why |
|---|---|---|
| OpenAI (`OPENAI_API_KEY`, gpt-4o) | Anthropic Claude (`ANTHROPIC_API_KEY`, Haiku 4.5) | Fits the role and topic; uses a current Claude model |
| BM25 retrieval over runbooks | Dictionary + LLM + vision extraction | Different domain (clinical coding, not incident triage) |
| 3 tiers = autonomy ladder (router→planner→ReAct) | 3 eras = maturity ladder (rule-based→LLM→multimodal) | Same "measurable progression" framing, mapped to Clinical NLP |
| 4 per-tier notebooks | 1 guided notebook | One coherent walkthrough is enough for this scope |
| LLM-as-judge eval | Gold-set precision/recall + status accuracy | The clinical task has a checkable gold answer |

## Added (submission-specific, not in the reference)

| This repo has | Why |
|---|---|
| `deliverables/` (report.docx, slides.pptx, video/) | The Cotiviti assessment requires a report, slides, and a video — the reference is not a job submission |
| APA report + slide deck | Required deliverables |

## One-line summary

This repo adopts the reference's professional Python conventions wholesale
(`src/` + Typer + `prompts/*.yaml` + `config.py` + pydantic + CI + evaluation +
BENCHMARKS/WHAT_BROKE), swaps the domain and provider to fit Topic 1 on Claude,
and adds the submission deliverables the assessment requires.
