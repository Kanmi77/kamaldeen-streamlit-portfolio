from __future__ import annotations

import streamlit as st

from portfolio import IMAGES, header, timeline_item

header(
    "Professional journey",
    "Experience",
    "Roles across bioinformatics, scientific teaching, operational analytics, microbiological research, clinical laboratory exposure and pharmaceutical quality control.",
)

st.markdown('<div class="timeline">', unsafe_allow_html=True)
timeline_item(
    "Nov 2025–Present",
    "Research Assistant – Bioinformatics",
    "Bayerisches Zentrum für Innovative Lehre (BayZiel) · Bavaria, Germany",
    "Develop reproducible Python and R workflows for biological data curation, protein feature extraction, structural analysis and machine-learning-supported candidate prioritisation.",
)
timeline_item(
    "Apr 2022–Present",
    "Assistant Lecturer",
    "Moshood Abiola Polytechnic · Remote",
    "Deliver microbiology and life-science instruction, supervise student projects and support experimental planning, data interpretation and scientific report writing.",
)
timeline_item(
    "Dec 2021–Jun 2023",
    "Data Analyst",
    "MTN · Lagos, Nigeria",
    "Cleaned and analysed operational data, applied statistical and machine-learning methods and communicated findings through reports, presentations and visual outputs.",
)
timeline_item(
    "Dec 2021–Jan 2022",
    "Research Apprentice – Microbiological Assays",
    "Prof. Lateef Agbaje Bio-Nanotechnology Laboratory · Nigeria",
    "Supported sample preparation, microbial testing, antibacterial-activity research, documentation and safe laboratory practice.",
)
timeline_item(
    "Apr 2020–Dec 2021",
    "Laboratory Assistant",
    "Central Research Laboratories, University of Ilorin · Nigeria",
    "Supported microbiological, molecular and analytical workflows involving sample preparation, PCR, gel electrophoresis, microscopy and analytical instruments.",
)
timeline_item(
    "2020",
    "Clinical Laboratory Intern",
    "Dr. Hammond Clinic · Nigeria",
    "Supported clinical laboratory and microscopy activities while following PPE, hygiene, sample-handling and documentation requirements.",
)
timeline_item(
    "Jul 2018–Nov 2019",
    "Laboratory Assistant – Pharmaceutical Quality Control",
    "Mopsin Pharmaceuticals Limited · Lagos, Nigeria",
    "Supported assigned QC activities, sample preparation, water-quality checks, SOP compliance, hygiene and traceable laboratory documentation.",
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("## Selected work evidence")
st.caption("Historical workplace photographs are used as supporting evidence. No confidential records or identifiable patient information are displayed.")

rows = [
    [
        ("bayziel.webp", "Computational research and biological data analysis at BayZiel, Germany."),
        ("agbaje-team.webp", "Professor Lateef Agbaje with members of the Bio-Nanotechnology Laboratory team."),
        ("mopsin.webp", "Pharmaceutical production and quality-control environment at Mopsin."),
    ],
    [
        ("uilorin-gc.webp", "Gas chromatography and analytical laboratory exposure at the Central Research Laboratories."),
        ("uilorin-ultrasonic.webp", "Ultrasonic sample-preparation equipment used in the analytical laboratory."),
        ("uilorin-analytics.webp", "Computer-connected spectrophotometer and result review."),
    ],
    [
        ("dr_hammond_1.jpg", "Clinical microscopy activity at Dr. Hammond Clinic."),
        ("dr_hammond_2.jpg", "Laboratory microscopy and sample examination."),
        ("dr_hammond_3.jpg", "Clinical laboratory practice using a compound microscope and appropriate PPE."),
    ],
]

for row in rows:
    cols = st.columns(3, gap="medium")
    for col, (filename, caption) in zip(cols, row):
        with col:
            st.image(IMAGES / filename, use_container_width=True)
            st.markdown(f'<div class="photo-caption">{caption}</div>', unsafe_allow_html=True)

st.markdown("## Education")
e1, e2, e3 = st.columns(3, gap="large")
with e1:
    st.markdown("### MSc Life Science Informatics")
    st.markdown("**Deggendorf Institute of Technology, Germany**  ")
    st.markdown("2024–2026")
    st.caption("Bioinformatics, biological data analysis, machine learning, NGS, multi-omics and scientific documentation.")
with e2:
    st.markdown("### Diploma in Data Science")
    st.markdown("**GOMYCODE, Nigeria**  ")
    st.markdown("2023")
    st.caption("Python, data processing, machine learning and analytical project work.")
with e3:
    st.markdown("### BSc Microbiology")
    st.markdown("**Summit University, Nigeria**  ")
    st.markdown("2017–2021 · First Class Honours")
    st.caption("Best Graduating Student, Department of Microbiology and Faculty of Life Science.")

st.markdown("## Languages")
st.markdown("**English:** C1 professional proficiency · **German:** A2 · **Yoruba:** Native")
