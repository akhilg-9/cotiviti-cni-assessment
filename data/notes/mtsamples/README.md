# MTSamples test notes

Five de-identified transcription samples from [MTSamples.com](https://www.mtsamples.com)
(public teaching corpus; each file's `Source:` header links the original page).
Chosen for condition variety: cardiac, endocrine, oncology, and multi-morbidity
follow-ups.

| File | Case | Rules found | LLM found (live) |
|---|---|--:|--:|
| `af_soap.txt` | Post-AVR atrial fibrillation, WPW | 2 (1 wrong¹) | 11 |
| `anemia_leukemia_followup.txt` | CLL + autoimmune hemolytic anemia | **0** | 8 |
| `cad_followup.txt` | CAD + anxiety, multi-morbidity | 1 | 16 |
| `cardiology_progress.txt` | Essential hypertension w/u | 1 | 3 |
| `hypothyroid_followup.txt` | Hypothyroidism, s/p thyroid cancer | 1 | 4 |

¹ The note says a catheterization showed "**no evidence of** coronary artery
disease" — the rule-based negation heuristic misses it and reports CAD as
*active*; the LLM correctly omits it. A live false positive that illustrates
exactly the brittleness described in the report.

Run any of them:

```bash
python -m src.cli run data/notes/mtsamples/anemia_leukemia_followup.txt
```
