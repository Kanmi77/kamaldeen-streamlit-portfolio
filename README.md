# Kamaldeen Olasunkanmi Bada — Scientific and Data Portfolio

A multipage Streamlit portfolio presenting verified evidence across bioinformatics, computational biology, data analytics, environmental microbiology, reproducible workflows, laboratory quality and scientific communication.

## Main navigation

- **Home** — professional identity plus interactive featured analytical work
- **Project Explorer** — equal access to six project areas, with no default project prioritised
- **Experience** — professional timeline and selected workplace evidence
- **Skills** — capabilities organised by professional function
- **CV & Contact** — downloadable CV and professional contact links

## Project Explorer coverage

1. **Xylanase Thermostability Research** — candidate landscape, evidence integration, parallel coordinates, MD heatmap and filtered downloads
2. **Afelele Environmental & Metagenomic Assessment** — Proteobacteria community shifts, selected-genus heatmap, heavy-metal panels and physicochemical exploration
3. **Reproducible RNA-seq Workflow** — documented six-sample pipeline, implementation evidence and downloadable workflow template
4. **Breast Cancer Diagnostic Data Analysis** — PCA, selectable distributions, correlation analysis, relationship exploration and corrected Excel dashboard
5. **Operational Data Analysis & Decision Support** — confidentiality-aware professional case study
6. **Laboratory Quality & Microbiology Practice** — clinical, pharmaceutical, environmental and research-laboratory evidence

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Use:

- Repository: `Kanmi77/kamaldeen-streamlit-portfolio`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Recommended Python version: `3.12`

Upload the **contents** of this extracted package to the repository root. Preserve `pages/`, `data/`, `assets/` and `.streamlit/` as folders.

## Language

German proficiency is shown as **A2**.

## Privacy and scientific scope

- No confidential employer data, patient information or protected sample identifiers are published.
- Computational predictions are not presented as experimental confirmation.
- Healthcare analysis is descriptive and exploratory, not a diagnostic or clinical-decision tool.
- Public claims are restricted to supplied data and documented evidence.


## July 2026 maintenance update

- Identified the photographed computer-connected analytical instrument as a spectrophotometer.
- Added explicit unique Streamlit keys to all Plotly elements to prevent duplicate element-ID failures when charts appear in multiple tabs.
