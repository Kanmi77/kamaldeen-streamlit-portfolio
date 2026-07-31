from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
required = [
    ROOT / "streamlit_app.py",
    ROOT / "portfolio.py",
    ROOT / "requirements.txt",
    ROOT / "DATA_PROVENANCE.md",
    ROOT / "pages" / "home.py",
    ROOT / "pages" / "project_explorer.py",
    ROOT / "pages" / "experience.py",
    ROOT / "pages" / "skills.py",
    ROOT / "pages" / "cv_contact.py",
    ROOT / "data" / "xylanase_candidate_rankings.csv",
    ROOT / "data" / "xylanase_md_temperature_delta.csv",
    ROOT / "data" / "afelele_heavy_metals.csv",
    ROOT / "data" / "afelele_proteobacteria_classes.csv",
    ROOT / "data" / "afelele_selected_genera.csv",
    ROOT / "data" / "rnaseq_evidence_summary.csv",
    ROOT / "data" / "breast_cancer_cleaned_568.csv",
    ROOT / "data" / "breast_cancer_feature_summary.csv",
    ROOT / "assets" / "downloads" / "Kamaldeen_Breast_Cancer_Data_Analysis_Cleaned.xlsx",
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit("Missing files: " + ", ".join(missing))

rankings = pd.read_csv(ROOT / "data" / "xylanase_candidate_rankings.csv")
assert len(rankings) == 2954
assert set(rankings["branch"].unique()) == {"Homology", "PDB"}

heavy = pd.read_csv(ROOT / "data" / "afelele_heavy_metals.csv")
classes = pd.read_csv(ROOT / "data" / "afelele_proteobacteria_classes.csv")
genera = pd.read_csv(ROOT / "data" / "afelele_selected_genera.csv")
assert len(heavy) == 10
assert len(classes) == 5
assert len(genera) == 10

rna = pd.read_csv(ROOT / "data" / "rnaseq_evidence_summary.csv")
assert int(rna.set_index("metric").loc["paired_end_samples", "value"]) == 6

breast = pd.read_csv(ROOT / "data" / "breast_cancer_cleaned_568.csv")
assert len(breast) == 568
assert breast["Diagnosis"].value_counts().to_dict() == {"Benign": 357, "Malignant": 211}
assert int(breast["Area Mean"].isna().sum()) == 1
assert int(breast["Patient ID"].duplicated().sum()) == 0

app_text = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")
home_text = (ROOT / "pages" / "home.py").read_text(encoding="utf-8")
explorer_text = (ROOT / "pages" / "project_explorer.py").read_text(encoding="utf-8")
assert "Project Explorer" in app_text
assert not (ROOT / "pages" / "xylanase_explorer.py").exists()
assert "Principal-component view" in home_text
assert "Proteobacteria community shift" in home_text
assert "xylanase_parallel_coordinates" in explorer_text
assert "afelele_genus_heatmap" in explorer_text
assert "breast_cancer_pca" in explorer_text
assert "index=None" in explorer_text

all_python = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.py") if path.name != "validate_package.py")
assert "German - B1" not in all_python
assert "German – B1" not in all_python
assert "Project standard used across this portfolio" not in all_python
assert "Evidence level" not in all_python
assert ("This version presents the common " + "professional thread") not in all_python
assert ("Specialised CVs remain " + "more appropriate") not in all_python

print("Validation passed: all six project areas, advanced analytical views, required data and A2 language setting are present.")
