# Real Clinical Note PDFs (publicly available, de-identified)

Real-world sample clinical notes downloaded from public medical-education and
health-system sources on 2026-07-23. All are de-identified teaching samples
(fictional/redacted patients) — no real PHI — so they are safe to commit and test with.

The current pipeline (`clinical-notes run <file>`) reads plain text, so each PDF's
text has been extracted to `extracted_text/<name>.txt`. Use the PDFs themselves
for future PDF-ingestion / vision (LMM) testing — several have realistic EHR layout.

| File | Type | Source |
|---|---|---|
| `ucf_adult_history_physical.pdf` | Comprehensive adult H&P, 48 y/o male, RA + anemia workup (6 pp) | [UCF College of Medicine](https://med.ucf.edu/media/2018/08/Sample-Adult-History-And-Physical-By-M2-Student.pdf) |
| `uhn_discharge_summary_medicine.pdf` | Internal-medicine discharge summary, pyelonephritis, realistic EHR printout format (3 pp) | [University Health Network, Toronto](https://www.uhnmodules.ca/DischargeSummary/assets/Good%20Discharge%20Summary%20Sample%20-Medicine.pdf) |
| `schulich_admission_progress_discharge_notes.pdf` | Bundle: admission note + CTU progress note + discharge summary (29 pp) | [Schulich School of Medicine, Western University](https://www.schulich.uwo.ca/cquins/docs/Sample-Progress-Notes-and-DC-Note-Brochure-1.pdf) |
| `icanotes_psych_discharge_summary.pdf` | Inpatient psychiatric discharge summary, EHR-generated (2 pp) | [ICANotes](https://www.icanotes.com/wp-content/uploads/2020/11/Inpatient%20Psychiatric%20Treatment%20Discharge%20Summary%20Sample.pdf) |
| `samdia_15_soap_examples.pdf` | 15 filled-in SOAP notes across specialties (psych, PT, nursing, …) (13 pp) | [Samdia / Carepatron](https://www.samdia.com/wp-content/uploads/2024/09/15-SOAP-NOTE-EXAMPLES-for-VARIOUS-PRACTITIONERS.pdf) |
| `maryland_soap_note.pdf` | Acupuncture SOAP note with filled-in "Jane Doe" case (pp 2–4) | [Maryland Dept. of Health](https://health.maryland.gov/bacc/Documents/SOAP%20Note%20Template.pdf) |

## Quick test

```bash
python demo.py data/notes/real_pdfs/extracted_text/uhn_discharge_summary_medicine.txt
# or
python -m src.cli run data/notes/real_pdfs/extracted_text/ucf_adult_history_physical.txt
```

## Notes for larger corpora

- **MTSamples** (mtsamples.com): thousands of real transcribed sample notes, HTML only (no PDFs).
- **MIMIC-IV / MIMIC-III** (physionet.org): real de-identified ICU notes at scale — requires free credentialed access + data-use agreement; cannot be committed to a public repo.
