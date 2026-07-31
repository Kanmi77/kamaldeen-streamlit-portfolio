from __future__ import annotations

import streamlit as st

from portfolio import card, header, tags

header(
    "Capability map",
    "Skills and tools",
    "Capabilities are grouped by function and supported by projects or workplace experience rather than presented as an undifferentiated keyword list.",
)

c1, c2 = st.columns(2, gap="large")
with c1:
    card(
        "Bioinformatics & computational biology",
        "Biological data curation, sequence analysis, multiple-sequence alignment, structural bioinformatics, protein modelling, mutation-stability assessment, molecular docking, molecular dynamics, RNA-seq and multi-omics analysis.",
        "Scientific computing",
    )
    tags(["Python", "R", "Biopython", "BLAST", "MAFFT", "FastTree", "MODELLER", "FoldX", "AutoDock Vina", "PyMOL", "Snakemake", "Git"])
with c2:
    card(
        "Data science & analytics",
        "Data cleaning, validation, exploratory analysis, statistical comparison, regression, classification, feature engineering, model evaluation, forecasting, visualisation and decision-ready reporting.",
        "Analytical practice",
    )
    tags(["Python", "R", "SQL", "pandas", "NumPy", "scikit-learn", "Matplotlib", "Excel", "Power BI"])

c3, c4 = st.columns(2, gap="large")
with c3:
    card(
        "Microbiology & molecular biology",
        "Microbiological assays, aseptic technique, sample and media preparation, microbial culture, antibacterial-activity testing, PCR, gel electrophoresis, cell-culture support, microscopy and metagenomic investigation.",
        "Laboratory science",
    )
    tags(["Microbiology", "PCR", "Gel electrophoresis", "Microscopy", "Sample handling", "Metagenomics", "Antimicrobial assays"])
with c4:
    card(
        "Quality, research & communication",
        "SOP-based work, pharmaceutical QC support, traceability, contamination control, laboratory safety, scientific writing, technical reporting, presentations, teaching, research supervision and stakeholder communication.",
        "Transferable value",
    )
    tags(["SOP compliance", "Data integrity", "QC documentation", "Scientific writing", "Teaching", "Research supervision", "Technical communication"])

st.markdown("## Analytical laboratory exposure")
st.markdown(
    "Practical or supervised use of atomic absorption spectrophotometry, gas chromatography, absorbance measurement, ultrasonic sample preparation and compound microscopy. These are described as documented exposure—not inflated independent mastery."
)

st.markdown("## How employers can read this skill set")
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    card("Research roles", "Bioinformatics, computational biology, microbiology, molecular biology, scientific data analysis and research support.")
with col2:
    card("Data roles", "Data science, research analytics, operational analytics, public-health analytics and decision-support functions.")
with col3:
    card("Quality and commercial roles", "QC/QA, technical sales, scientific product support and roles requiring clear translation of technical evidence.")

