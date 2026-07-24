"""
Tiny clinical terminology reference for the demo.

Maps common conditions to an ICD-10 code and the CMS-HCC risk-adjustment
category they typically fall into. Real systems use full SNOMED CT / ICD-10-CM
terminologies with tens of thousands of codes; this curated slice is enough to
prove the concept on the sample notes.

Each entry: canonical name -> {icd10, hcc, synonyms}
`synonyms` drives the rule-based ("Past") matcher.
"""

CONDITIONS = {
    "Type 2 diabetes mellitus": {
        "icd10": "E11.9",
        "hcc": "HCC 38 (Diabetes)",
        "synonyms": ["type 2 diabetes", "type 2 diabetes mellitus", "t2dm", "diabetes mellitus", "diabetes"],
    },
    "Congestive heart failure": {
        "icd10": "I50.9",
        "hcc": "HCC 226 (Heart Failure)",
        "synonyms": ["congestive heart failure", "chf", "heart failure"],
    },
    "Chronic obstructive pulmonary disease": {
        "icd10": "J44.9",
        "hcc": "HCC 280 (COPD)",
        "synonyms": ["chronic obstructive pulmonary disease", "copd"],
    },
    "Chronic kidney disease, stage 3": {
        "icd10": "N18.30",
        "hcc": "HCC 329 (CKD stage 3)",
        "synonyms": ["chronic kidney disease, stage 3", "chronic kidney disease stage 3", "ckd stage 3", "ckd, stage 3", "ckd"],
    },
    "Coronary artery disease": {
        "icd10": "I25.10",
        "hcc": "HCC 263 (Atherosclerosis)",
        "synonyms": ["coronary artery disease", "cad"],
    },
    "Atrial fibrillation": {
        "icd10": "I48.91",
        "hcc": "HCC 264 (Arrhythmias)",
        "synonyms": ["atrial fibrillation", "afib", "a-fib"],
    },
    "Major depressive disorder": {
        "icd10": "F33.9",
        "hcc": "HCC 155 (Depression)",
        "synonyms": ["major depressive disorder", "major depression", "depression", "mdd"],
    },
    "Morbid obesity": {
        "icd10": "E66.01",
        "hcc": "HCC 48 (Morbid Obesity)",
        "synonyms": ["morbid obesity", "morbidly obese"],
    },
    "Essential hypertension": {
        "icd10": "I10",
        "hcc": "(not HCC-weighted)",
        "synonyms": ["hypertension", "htn", "high blood pressure"],
    },
}

# Negation / non-active cues for the rule-based matcher.
NEGATION_CUES = ["no ", "denies", "without", "negative for", "no history of", "ruled out", "not yet confirmed", "suspected"]
