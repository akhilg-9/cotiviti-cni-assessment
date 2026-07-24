"""
Streamlit UI for the Clinical Note Intelligence POC.

Run:
    streamlit run app.py

Shows the Past -> Present -> Future progression side by side on a clinical note,
which makes a clean screen-share for the demo video.
"""

import os

import streamlit as st

from src import llm_extract, rules_ner, scan, vision_extract
from src.config import have_api_key, model

HERE = os.path.dirname(__file__)
NOTES_DIR = os.path.join(HERE, "data", "notes")

st.set_page_config(page_title="Clinical Note Intelligence", layout="wide")
st.title("🩺 Clinical Note Intelligence")
st.caption(
    "Topic 1 — Clinical NLP · Past → Present → Future. "
    "Turns an unstructured clinical note into codeable ICD-10 / HCC findings."
)

# --- mode banner -----------------------------------------------------------
if have_api_key():
    st.success(f"LIVE mode — calling Claude ({model()}).")
else:
    st.warning(
        "OFFLINE simulation — no ANTHROPIC_API_KEY set. The Present/Future panels "
        "approximate the LLM with the rule-based pass. Set a key for live results."
    )

# --- note selection --------------------------------------------------------
samples = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith(".txt"))
col_sel, _ = st.columns([1, 2])
with col_sel:
    choice = st.selectbox("Sample note", samples)

with open(os.path.join(NOTES_DIR, choice)) as f:
    default_text = f.read()

note = st.text_area("Clinical note (editable)", value=default_text, height=240)


def render_panel(title, subtitle, findings):
    st.subheader(title)
    st.caption(subtitle)
    if not findings:
        st.info("No conditions found.")
        return
    rows = [
        {
            "Condition": f["name"],
            "ICD-10": f["icd10"],
            "Status": f["status"],
            "Confidence": round(float(f["confidence"]), 2),
            "Evidence": f.get("evidence", ""),
        }
        for f in findings
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)


if st.button("Extract conditions", type="primary"):
    c1, c2, c3 = st.columns(3)
    with c1:
        render_panel("Past", "Rule-based dictionary + negation (classic clinical NLP)",
                     rules_ner.extract(note))
    with c2:
        with st.spinner("Calling LLM..." if have_api_key() else "Simulating..."):
            render_panel("Present", "LLM structured extraction (Claude)",
                         llm_extract.extract(note))
    with c3:
        scan_path = os.path.join(NOTES_DIR, "scanned_note.png")
        scan_pages = scan.render_pages(note, scan_path)
        with st.spinner("Reading scanned image..." if have_api_key() else "Simulating..."):
            findings = vision_extract.extract(scan_pages, offline_text=note)
        render_panel("Future / LMM", "Multimodal vision on a scanned image",
                     findings)
        with st.expander("Scanned image sent to the model"):
            for p in scan_pages:
                st.image(p, use_container_width=True)

st.divider()
st.caption("Synthetic notes only — no real PHI. Demonstrator prototype, not for clinical use.")
