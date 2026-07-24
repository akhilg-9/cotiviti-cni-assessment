.PHONY: install test demo demo-real eval app

install:            ## create venv-agnostic install (run inside your venv)
	pip install -r requirements.txt

test:               ## run the unit tests
	python -m pytest tests -q

demo:               ## three-era extraction on the synthetic note (live if ANTHROPIC_API_KEY set)
	python -m src.cli run data/notes/note1.txt

demo-real:          ## same pipeline on a real de-identified discharge summary
	python -m src.cli run data/notes/real_pdfs/extracted_text/uhn_discharge_summary_medicine.txt

eval:               ## score Past vs Present on the labeled gold set
	python -m src.cli eval

app:                ## interactive Streamlit demo
	streamlit run app.py
