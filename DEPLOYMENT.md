# Streamlit Deployment

## Repository structure

The repository root must contain:

```text
streamlit_app.py
portfolio.py
requirements.txt
pages/
data/
assets/
.streamlit/
```

## Replace the current repository contents

1. Extract the final ZIP.
2. Open the extracted folder.
3. In GitHub, upload the folders and files while preserving their structure.
4. Confirm that GitHub shows paths such as:
   - `pages/project_explorer.py`
   - `data/xylanase_candidate_rankings.csv`
   - `data/afelele_proteobacteria_classes.csv`
   - `data/breast_cancer_cleaned_568.csv`
   - `assets/downloads/Kamaldeen_Breast_Cancer_Data_Analysis_Cleaned.xlsx`
5. Commit directly to `main`.

Do not upload only the ZIP file, and do not flatten the `pages`, `data`, `assets` or `.streamlit` folders.

## Streamlit Community Cloud

- Repository: `Kanmi77/kamaldeen-streamlit-portfolio`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Recommended Python: `3.12`

After the commit, open **Manage app → Reboot app**. If necessary, clear the app cache.

## File discovery

The app searches the intended folder first, then the repository root and one or more nested paths. This helps with common GitHub upload mistakes, but the full extracted package should still be uploaded because the Home page and Project Explorer rely on several project datasets.

## Corrective deployment note

This V3.1 package replaces the previous Analytics V3 package. Upload the revised `pages/home.py`, `pages/project_explorer.py`, and `pages/experience.py` together with the complete package, then use **Manage app → Reboot app**.
