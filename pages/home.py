from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from portfolio import (
    EMAIL,
    GITHUB,
    LINKEDIN,
    card,
    data_file,
    image_file,
    project_card,
    show_missing_file_error,
    tags,
)


def read_csv(filename: str) -> pd.DataFrame:
    try:
        return pd.read_csv(data_file(filename))
    except FileNotFoundError as error:
        show_missing_file_error(error)
        raise


def breast_cancer_pca(data: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    numeric = data.select_dtypes(include=[np.number]).drop(columns=["Patient ID"], errors="ignore")
    numeric = numeric.apply(lambda column: column.fillna(column.median()))
    means = numeric.mean(axis=0)
    scales = numeric.std(axis=0, ddof=0).replace(0, 1)
    standardised = (numeric - means) / scales
    u, singular_values, _ = np.linalg.svd(standardised.to_numpy(), full_matrices=False)
    scores = u[:, :2] * singular_values[:2]
    variance = singular_values**2
    explained = variance / variance.sum()
    result = pd.DataFrame({"PC1": scores[:, 0], "PC2": scores[:, 1]})
    result["Diagnosis"] = data["Diagnosis"].to_numpy()
    result["Patient ID"] = data["Patient ID"].astype(str).to_numpy()
    result["Radius Mean"] = data["Radius Mean"].to_numpy()
    result["Area Mean"] = data["Area Mean"].to_numpy()
    return result, explained


def afelele_class_shift(classes: pd.DataFrame) -> go.Figure:
    ordered = classes.sort_values("surface_water_percent", ascending=True)
    fig = go.Figure()
    for _, row in ordered.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["surface_water_percent"], row["sediment_percent"]],
                y=[row["class"], row["class"]],
                mode="lines",
                line={"width": 2},
                hoverinfo="skip",
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=ordered["surface_water_percent"],
            y=ordered["class"],
            mode="markers",
            name="Surface water",
            marker={"size": 12},
            customdata=ordered[["surface_water_reads"]],
            hovertemplate="%{y}<br>Surface water: %{x:.2f}%<br>Reads: %{customdata[0]:,.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ordered["sediment_percent"],
            y=ordered["class"],
            mode="markers",
            name="Sediment",
            marker={"size": 12, "symbol": "diamond"},
            customdata=ordered[["sediment_reads"]],
            hovertemplate="%{y}<br>Sediment: %{x:.2f}%<br>Reads: %{customdata[0]:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Proteobacteria community shift between sample matrices",
        xaxis_title="Share of reported Proteobacteria reads (%)",
        yaxis_title="",
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"orientation": "h", "y": 1.12},
        margin={"l": 10, "r": 10, "t": 85, "b": 40},
    )
    return fig


left, right = st.columns([1.55, 0.75], gap="large", vertical_alignment="center")
with left:
    st.markdown('<div class="availability">Bavaria, Germany · Open to relevant opportunities</div>', unsafe_allow_html=True)
    st.markdown("# Kamaldeen Olasunkanmi Bada")
    st.markdown(
        '<div class="hero-role">Bioinformatics · Computational Biology · Data Analytics · Microbiology · Laboratory Quality</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-copy">I combine biological understanding, computational analysis and quality-focused laboratory experience to build reproducible workflows, interrogate complex datasets and communicate decision-ready findings.</p>',
        unsafe_allow_html=True,
    )
    b1, b2, b3 = st.columns(3)
    with b1:
        st.page_link("pages/project_explorer.py", label="Project Explorer", icon="🗂️", use_container_width=True)
    with b2:
        st.link_button("LinkedIn", LINKEDIN, icon="↗", use_container_width=True)
    with b3:
        st.link_button("GitHub", GITHUB, icon="↗", use_container_width=True)
with right:
    try:
        st.image(image_file("portrait.webp"), caption="Kamaldeen Olasunkanmi Bada", use_container_width=True)
    except FileNotFoundError:
        st.info("Professional portrait")

st.markdown("## Professional identity")
st.markdown(
    "My work connects **life-science research, data-driven decision support and quality-conscious laboratory practice**. "
    "The portfolio presents real datasets, documented methods, interactive analytical views, reproducible workflows and selected laboratory evidence."
)

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    card(
        "Science & research",
        "Bioinformatics, computational biology, protein modelling, microbiology, molecular biology, environmental research and scientific teaching.",
        "Pathway 01",
    )
with c2:
    card(
        "Data & analytics",
        "Python, R, SQL, statistical analysis, multivariate exploration, data quality, visualisation and operational decision support.",
        "Pathway 02",
    )
with c3:
    card(
        "Quality & technical communication",
        "Pharmaceutical QC support, SOP-based documentation, laboratory safety, stakeholder communication and technical-commercial potential.",
        "Pathway 03",
    )

st.markdown("## Featured analytical work")
st.markdown(
    "These views are calculated from the packaged project data. They are designed to show analytical reasoning, not merely project decoration."
)

xylanase = read_csv("xylanase_candidate_rankings.csv")
afelele_classes = read_csv("afelele_proteobacteria_classes.csv")
breast = read_csv("breast_cancer_cleaned_568.csv")
rnaseq_steps = read_csv("rnaseq_pipeline_steps.csv")

x_tab, a_tab, b_tab, r_tab = st.tabs(["Xylanase", "Afelele", "Breast cancer", "RNA-seq"])

with x_tab:
    top = xylanase.sort_values("rank").head(150).copy()
    top["candidate"] = top["accession"].astype(str) + " " + top["mutation"].astype(str)
    top["retention_marker"] = top["retention_fraction"].fillna(0) + 0.12
    fig = px.scatter(
        top,
        x="foldx_ddg",
        y="integrated_score",
        size="retention_marker",
        color="branch",
        symbol="gh_family",
        hover_name="candidate",
        hover_data={
            "rank": True,
            "evidence_tier": True,
            "retention_fraction": ":.1f",
            "foldx_ddg": ":.3f",
            "integrated_score": ":.3f",
            "retention_marker": False,
        },
        title="Multi-evidence landscape of the 150 highest-priority candidates",
        labels={"foldx_ddg": "FoldX ΔΔG", "integrated_score": "Integrated evidence score"},
        size_max=18,
    )
    fig.add_vline(x=0, line_dash="dash")
    fig.update_layout(height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="home_xylanase_featured_chart")
    st.caption("Marker size reflects ligand-retention evidence. Negative FoldX ΔΔG indicates predicted stabilisation, not experimental confirmation.")

with a_tab:
    water_total = int(afelele_classes["surface_water_reads"].sum())
    sediment_total = int(afelele_classes["sediment_reads"].sum())
    m1, m2, m3 = st.columns(3)
    m1.metric("Surface-water reads", f"{water_total:,}")
    m2.metric("Sediment reads", f"{sediment_total:,}")
    m3.metric("Classes compared", len(afelele_classes))
    st.plotly_chart(afelele_class_shift(afelele_classes), use_container_width=True, config={"displaylogo": False}, key="home_afelele_class_shift_chart")
    st.caption("The connected-dot view reveals how community composition changes between surface water and sediment more clearly than a grouped bar chart.")

with b_tab:
    pca, explained = breast_cancer_pca(breast)
    fig = px.scatter(
        pca,
        x="PC1",
        y="PC2",
        color="Diagnosis",
        hover_name="Patient ID",
        hover_data={"Radius Mean": ":.3f", "Area Mean": ":.1f"},
        title=f"Principal-component view of 30 numeric measurements · PC1 {explained[0]:.1%}, PC2 {explained[1]:.1%}",
        labels={"PC1": f"PC1 ({explained[0]:.1%})", "PC2": f"PC2 ({explained[1]:.1%})"},
        opacity=0.72,
    )
    fig.update_traces(marker={"size": 8})
    fig.update_layout(height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="home_breast_cancer_pca_chart")
    st.caption("One missing Area Mean value is median-imputed only for this PCA calculation. The view is exploratory and is not a diagnostic model.")

with r_tab:
    st.markdown("### Reproducible RNA-seq workflow")
    ordered_steps = rnaseq_steps.sort_values("order").reset_index(drop=True)
    for start in range(0, len(ordered_steps), 3):
        cols = st.columns(3, gap="large")
        for col, (_, row) in zip(cols, ordered_steps.iloc[start:start + 3].iterrows()):
            with col:
                card(row["stage"], row["documented_output"], f"{int(row['order']):02d} · {row['tool']}")
    st.caption("The workflow coordinates quality control, trimming, alignment, quantification, differential-expression analysis and rule-based orchestration.")

st.page_link("pages/project_explorer.py", label="Open detailed access to every project", icon="🗂️", use_container_width=True)

st.markdown("## Project portfolio")
project_rows = [
    (
        "Computational biology",
        "Xylanase Thermostability Research",
        "Multi-source candidate ranking, structural validation, docking evidence and molecular-dynamics comparison.",
        "Interactive evidence landscape, parallel-coordinates analysis, MD heatmap and downloadable candidate tables.",
    ),
    (
        "Environmental microbiology",
        "Afelele Environmental & Metagenomic Assessment",
        "Physicochemical, heavy-metal and Proteobacteria evidence comparing surface water and sediment.",
        "Community-shift analysis, genus heatmap, concentration panels, data tables and field evidence.",
    ),
    (
        "Healthcare analytics",
        "Breast Cancer Diagnostic Data Analysis",
        "A corrected 568-record Excel analysis with transparent data-quality controls.",
        "PCA, selectable feature distributions, correlation analysis, scatter exploration and cleaned downloads.",
    ),
    (
        "Transcriptomics",
        "Reproducible RNA-seq Workflow",
        "A documented paired-end workflow from FastQC through DESeq2 with Snakemake orchestration.",
        "Pipeline evidence, implementation extracts, downloadable workflow template and stated limitations.",
    ),
    (
        "Operational analytics",
        "Data Analysis & Decision Support",
        "Professional experience cleaning and interpreting operational datasets for stakeholder reporting.",
        "A confidentiality-aware case study documenting methods, quality controls and communication practice.",
    ),
    (
        "Laboratory quality",
        "Microbiology, Clinical Laboratory & Pharmaceutical QC",
        "Documented experience in sample handling, microscopy, assays, analytical-laboratory practice and SOP-based quality work.",
        "Scoped workplace evidence, experience records and professional captions without inflated instrument claims.",
    ),
]
for i in range(0, len(project_rows), 2):
    cols = st.columns(2, gap="large")
    for col, item in zip(cols, project_rows[i:i + 2]):
        with col:
            project_card(*item)

st.markdown("## Core capability map")
tags([
    "Python", "R", "SQL", "Statistical analysis", "Multivariate analysis", "Machine learning",
    "Structural bioinformatics", "FoldX", "MODELLER", "RNA-seq", "Snakemake", "Microbiology",
    "PCR", "Microscopy", "Pharmaceutical QC", "Scientific reporting", "Research supervision",
])

st.info(f"Professional enquiries: {EMAIL}")
