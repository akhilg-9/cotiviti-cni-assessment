.PHONY: install test demo demo-real eval validity app

# Use the project venv when it exists, plain python3 otherwise —
# so `make demo` works without activating anything.
PY := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
STREAMLIT := $(shell [ -x .venv/bin/streamlit ] && echo .venv/bin/streamlit || echo streamlit)

install:            ## install dependencies (into the active environment)
	pip install -r requirements.txt

test:               ## run the unit tests
	$(PY) -m pytest tests -q

demo:               ## three-era extraction on the synthetic note (live if ANTHROPIC_API_KEY set)
	$(PY) -m src.cli run data/notes/note1.txt

demo-real:          ## same pipeline on a real de-identified discharge summary
	$(PY) -m src.cli run data/notes/real_pdfs/extracted_text/uhn_discharge_summary_medicine.txt

eval:               ## score Past vs Present on the labeled gold set
	$(PY) -m src.cli eval

validity:           ## code-validity vs official ICD-10-CM across runs/ audit artifacts
	$(PY) -m src.cli validity

app:                ## interactive Streamlit demo
	$(STREAMLIT) run app.py
