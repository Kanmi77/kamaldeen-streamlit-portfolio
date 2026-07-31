from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from portfolio import (
    ASSETS,
    GITHUB,
    RESULTS_REPO,
    WORKFLOW_REPO,
    data_file,
    download_file,
    header,
    image_file,
    project_card,
    show_missing_file_error,
    tags,
)

PROJECTS = [
    "Xylanase Thermostability Research",
    "Afelele Environmental & Metagenomic Assessment",
    "Reproducible RNA-seq Workflow",
    "Breast Cancer Diagnostic Data Analysis",
    "Operational Data Analysis & Decision Support",
    "Laboratory Quality & Microbiology Practice",
]


def read_csv(filename: str) -> pd.DataFrame:
    try:
        return pd.read_csv(data_file(filename))
    except FileNotFoundError as error:
        show_missing_file_error(error)
        raise


def show_image(filename: str, subfolder: str | None = None, caption: str | None = None) -> None:
    try:
        st.image(image_file(filename, subfolder), caption=caption, use_container_width=True)
    except FileNotFoundError:
        st.caption(f"Image not available: {filename}")


def download_path(filename: str) -> Path | None:
    try:
        return download_file(filename)
    except FileNotFoundError:
        return None


def evidence_sections(
    problem: str,
    contribution: str,
    data: str,
    methods: str,
    quality: str,
    results: str,
    limitations: str,
    reproducibility: str,
) -> None:
    with st.expander("Problem and objective", expanded=True):
        st.markdown(problem)
    with st.expander("Personal contribution"):
        st.markdown(contribution)
    with st.expander("Data and evidence"):
        st.markdown(data)
    with st.expander("Methods and tools"):
        st.markdown(methods)
    with st.expander("Quality control"):
        st.markdown(quality)
    with st.expander("Results"):
        st.markdown(results)
    with st.expander("Limitations"):
        st.markdown(limitations)
    with st.expander("Reproducibility and access"):
        st.markdown(reproducibility)


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
        fig.add_trace(go.Scatter(
            x=[row["surface_water_percent"], row["sediment_percent"]],
            y=[row["class"], row["class"]], mode="lines",
            line={"width": 2}, hoverinfo="skip", showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=ordered["surface_water_percent"], y=ordered["class"],
        mode="markers", name="Surface water", marker={"size": 13},
        customdata=ordered[["surface_water_reads"]],
        hovertemplate="%{y}<br>Surface water: %{x:.2f}%<br>Reads: %{customdata[0]:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=ordered["sediment_percent"], y=ordered["class"],
        mode="markers", name="Sediment", marker={"size": 13, "symbol": "diamond"},
        customdata=ordered[["sediment_reads"]],
        hovertemplate="%{y}<br>Sediment: %{x:.2f}%<br>Reads: %{customdata[0]:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title="Proteobacteria community shift between sample matrices",
        xaxis_title="Share of reported Proteobacteria reads (%)", yaxis_title="",
        height=500, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend={"orientation": "h", "y": 1.12},
    )
    return fig


def afelele_genus_heatmap(genera: pd.DataFrame) -> go.Figure:
    matrix = genera.set_index("genus")[["surface_water_reads", "sediment_reads"]].copy()
    transformed = np.log1p(matrix.astype(float))
    fig = go.Figure(go.Heatmap(
        z=transformed.to_numpy(), x=["Surface water", "Sediment"], y=transformed.index,
        customdata=matrix.to_numpy(),
        hovertemplate="%{y}<br>%{x}: %{customdata:,.0f} reads<extra></extra>",
        colorbar={"title": "log(1 + reads)"},
    ))
    fig.update_layout(
        title="Selected-genus community fingerprint", height=520,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Sample matrix", yaxis_title="",
    )
    return fig


def afelele_metal_panels(heavy: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Surface water (mg/L)", "Sediment (mg/kg)"), shared_yaxes=True)
    water = heavy[~heavy["surface_water_not_detected"] & heavy["surface_water_mean"].notna()].copy()
    sediment = heavy[heavy["sediment_mean"].notna()].copy()
    fig.add_trace(go.Scatter(
        x=water["surface_water_mean"], y=water["metal"], mode="markers",
        error_x={"type": "data", "array": water["surface_water_sd"], "visible": True},
        customdata=water[["symbol"]],
        hovertemplate="%{y} (%{customdata[0]})<br>%{x:.4g} mg/L<extra></extra>",
        name="Surface water", marker={"size": 11},
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=sediment["sediment_mean"], y=sediment["metal"], mode="markers",
        error_x={"type": "data", "array": sediment["sediment_sd"], "visible": True},
        customdata=sediment[["symbol"]],
        hovertemplate="%{y} (%{customdata[0]})<br>%{x:.4g} mg/kg<extra></extra>",
        name="Sediment", marker={"size": 11, "symbol": "diamond"},
    ), row=1, col=2)
    fig.update_xaxes(type="log", row=1, col=1)
    fig.update_xaxes(type="log", row=1, col=2)
    fig.update_layout(
        title="Heavy-metal concentration profiles with reported uncertainty",
        height=560, showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def xylanase_parallel_coordinates(rankings: pd.DataFrame, top_n: int = 60) -> go.Figure:
    selected = rankings.sort_values("rank").head(top_n).copy()
    columns = ["integrated_score", "foldx_score", "docking_score", "ml_score", "retention_fraction"]
    for column in columns:
        selected[column] = pd.to_numeric(selected[column], errors="coerce")
    selected[columns] = selected[columns].fillna(selected[columns].median(numeric_only=True)).fillna(0)
    fig = px.parallel_coordinates(
        selected, dimensions=columns, color="integrated_score",
        labels={
            "integrated_score": "Integrated", "foldx_score": "FoldX",
            "docking_score": "Docking", "ml_score": "ML",
            "retention_fraction": "Retention",
        },
        title=f"Multi-evidence profiles for the top {top_n} ranked candidates",
    )
    fig.update_layout(height=560, paper_bgcolor="rgba(0,0,0,0)")
    return fig


def xylanase_md_heatmap(md_delta: pd.DataFrame) -> go.Figure:
    metrics = [
        "rmsd_mean_nm_delta_373_minus_333",
        "rmsf_mean_nm_delta_373_minus_333",
        "rg_mean_nm_delta_373_minus_333",
        "hbond_mean_delta_373_minus_333",
        "dssp_ordered_fraction_mean_delta_373_minus_333",
    ]
    labels = ["Δ RMSD", "Δ RMSF", "Δ Rg", "Δ H-bonds", "Δ ordered fraction"]
    matrix = md_delta.set_index("protein")[metrics].copy()
    standardised = (matrix - matrix.mean(axis=0)) / matrix.std(axis=0, ddof=0).replace(0, 1)
    fig = go.Figure(go.Heatmap(
        z=standardised.to_numpy(), x=labels, y=standardised.index,
        customdata=matrix.to_numpy(),
        hovertemplate="%{y}<br>%{x}: %{customdata:.4f}<extra></extra>",
        colorbar={"title": "Standardised change"}, zmid=0,
    ))
    fig.update_layout(
        title="Molecular-dynamics response from 333 K to 373 K", height=500,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_xylanase() -> None:
    rankings = read_csv("xylanase_candidate_rankings.csv")
    branch = read_csv("xylanase_branch_summary.csv")
    md = read_csv("xylanase_modeller_md_mean_metrics.csv")
    md_delta = read_csv("xylanase_md_temperature_delta.csv")
    tmalign = read_csv("xylanase_tmalign_summary.csv")

    rankings["organism"] = rankings["organism"].fillna("Not specified")
    rankings["md_level"] = rankings["md_level"].fillna("Not assessed")
    mean_tm = float(tmalign.set_index("metric").loc["mean_best_tm_score", "value"])

    st.markdown("## Xylanase Thermostability Research")
    st.markdown(
        '<div class="source-note">This project integrates several computational evidence streams. Negative FoldX ΔΔG is interpreted as predicted stabilisation, not experimental confirmation.</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Ranked candidates", f"{len(rankings):,}")
    m2.metric("Predicted stabilising", f"{int((rankings['foldx_ddg'] < 0).sum()):,}")
    m3.metric("Both ligands retained", f"{int((rankings['retention_fraction'] == 1).sum()):,}")
    m4.metric("Mean best TM-score", f"{mean_tm:.3f}")

    overview, landscape, integration, dynamics, documentation = st.tabs([
        "Overview", "Candidate landscape", "Evidence integration", "Molecular dynamics", "Methods & limitations"
    ])

    with overview:
        a, b = st.columns([1.05, 0.95], gap="large")
        with a:
            st.markdown(
                "The analysis combines mutation-stability estimates, ligand-retention evidence, machine-learning outputs, structural comparisons and temperature-dependent simulation metrics. "
                "Candidate ranking is therefore presented as a multi-criteria prioritisation problem rather than a single-score list."
            )
            tags(["Python", "R", "FoldX", "MODELLER", "Docking", "Molecular dynamics", "Machine learning", "Data integration"])
            branch_display = branch.rename(columns={
                "branch": "Structure branch", "candidates": "Candidates",
                "stabilising_candidates": "Predicted stabilising",
                "stabilising_percent": "Predicted stabilising (%)",
                "full_retention_percent": "Both ligands retained (%)",
            })
            st.dataframe(branch_display, hide_index=True, use_container_width=True)
        with b:
            top = rankings.sort_values("rank").head(120).copy()
            top["candidate"] = top["accession"].astype(str) + " " + top["mutation"].astype(str)
            top["retention_marker"] = top["retention_fraction"].fillna(0) + 0.12
            fig = px.scatter(
                top, x="foldx_ddg", y="integrated_score", size="retention_marker",
                color="branch", symbol="gh_family", hover_name="candidate",
                hover_data={"rank": True, "evidence_tier": True, "retention_fraction": ":.1f", "retention_marker": False},
                labels={"foldx_ddg": "FoldX ΔΔG", "integrated_score": "Integrated evidence score"},
                title="Highest-priority candidate landscape", size_max=17,
            )
            fig.add_vline(x=0, line_dash="dash")
            fig.update_layout(height=510, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="xyl_overview_candidate_chart")

    with landscape:
        f1, f2, f3 = st.columns(3)
        selected_gh = f1.multiselect(
            "GH family", sorted(rankings["gh_family"].dropna().unique()),
            default=sorted(rankings["gh_family"].dropna().unique()),
            key="xyl_gh",
        )
        selected_branch = f2.multiselect(
            "Structure branch", sorted(rankings["branch"].dropna().unique()),
            default=sorted(rankings["branch"].dropna().unique()),
            key="xyl_branch",
        )
        selected_tiers = f3.multiselect(
            "Evidence tier", sorted(rankings["evidence_tier"].dropna().unique()),
            default=sorted(rankings["evidence_tier"].dropna().unique()),
            key="xyl_tier",
        )
        c1, c2 = st.columns(2)
        minimum_retention = c1.select_slider("Minimum ligand retention", options=[0.0, 0.5, 1.0], value=0.0, key="xyl_retention")
        stabilising_only = c2.checkbox("Predicted stabilising only", value=True, key="xyl_stabilising")
        top_n = st.slider("Candidates to display", 20, 300, 100, 10, key="xyl_topn")

        filtered = rankings[
            rankings["gh_family"].isin(selected_gh)
            & rankings["branch"].isin(selected_branch)
            & rankings["evidence_tier"].isin(selected_tiers)
            & (rankings["retention_fraction"] >= minimum_retention)
        ].copy()
        if stabilising_only:
            filtered = filtered[filtered["foldx_ddg"] < 0]
        filtered = filtered.sort_values("rank").head(top_n)

        if filtered.empty:
            st.warning("No candidates match the selected filters.")
        else:
            filtered["candidate"] = filtered["accession"].astype(str) + " " + filtered["mutation"].astype(str)
            filtered["retention_marker"] = filtered["retention_fraction"].fillna(0) + 0.12
            fig = px.scatter(
                filtered, x="foldx_ddg", y="integrated_score", size="retention_marker",
                color="evidence_tier", symbol="branch", hover_name="candidate",
                hover_data=["organism", "gh_family", "md_level", "rank", "retention_fraction"],
                title="Filtered multi-evidence candidate landscape",
                labels={"foldx_ddg": "FoldX ΔΔG", "integrated_score": "Integrated evidence score"},
                size_max=18,
            )
            fig.add_vline(x=0, line_dash="dash")
            fig.update_layout(height=560, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="xyl_filtered_candidate_chart")
            columns = [
                "rank", "accession", "mutation", "organism", "gh_family", "branch",
                "evidence_tier", "integrated_score", "foldx_ddg", "retention_fraction", "md_level",
            ]
            st.dataframe(filtered[columns], hide_index=True, use_container_width=True)
            st.download_button(
                "Download filtered candidates", filtered.to_csv(index=False).encode("utf-8"),
                "xylanase_filtered_candidates.csv", "text/csv", icon="⬇️",
            )

    with integration:
        top_parallel = st.slider("Candidates in parallel-coordinates view", 20, 100, 60, 10, key="xyl_parallel_n")
        st.plotly_chart(xylanase_parallel_coordinates(rankings, top_parallel), use_container_width=True, config={"displaylogo": False}, key="xyl_parallel_coordinates_chart")
        st.caption("Each line is one candidate. The view reveals trade-offs among stability, docking, machine-learning and ligand-retention evidence.")
        visual_options = {
            "Top 15 ranked candidates": ("xylanase_top15_candidates.png", "Integrated scores displayed in supplied rank order."),
            "FoldX distribution": ("xylanase_foldx_distribution.png", "Distribution by PDB and homology-model branch."),
            "Docking retention": ("xylanase_docking_retention.png", "Retention categories calculated from the supplied retention field."),
            "Wild-type energy per residue": ("xylanase_wt_energy_per_residue.png", "Wild-type energy-per-residue distributions."),
        }
        selected_visual = st.selectbox("Supporting visual", list(visual_options), key="xyl_support_visual")
        filename, caption = visual_options[selected_visual]
        show_image(filename, "verified_results", caption)

    with dynamics:
        st.plotly_chart(xylanase_md_heatmap(md_delta), use_container_width=True, config={"displaylogo": False}, key="xyl_md_heatmap_chart")
        st.caption("Values are changes at 373 K relative to 333 K. The heatmap standardises metrics only for visual comparison; exact values remain available below.")
        metric = st.selectbox(
            "Inspect an MD metric",
            ["rmsd_mean_nm", "rmsf_mean_nm", "rg_mean_nm", "hbond_mean", "dssp_ordered_fraction_mean"],
            key="xyl_md_metric",
        )
        md_plot = md.copy()
        md_plot["system_label"] = md_plot["protein"] + " " + md_plot["state"]
        fig_md = px.line(
            md_plot.sort_values("temperature_K"), x="temperature_K", y=metric,
            color="system_label", markers=True, title=f"{metric} at 333 K and 373 K",
        )
        fig_md.update_layout(height=560, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_md, use_container_width=True, config={"displaylogo": False}, key="xyl_md_metric_chart")
        st.dataframe(md_delta, hide_index=True, use_container_width=True)

    with documentation:
        evidence_sections(
            "Prioritise candidate substitutions that may improve xylanase stability while retaining substrate-interaction evidence.",
            "Built and documented data-integration workflows; compared sequence, structure, FoldX, docking, machine-learning and MD evidence; generated ranked outputs and analytical visualisations.",
            f"The packaged ranking table contains {len(rankings):,} candidate records from homology-model and PDB-derived branches, supported by branch, docking, stability, structure-comparison and MD tables.",
            "Python/R data processing, structural bioinformatics, FoldX mutation assessment, docking comparison, machine-learning evidence integration, multivariate visualisation and temperature-comparison summaries.",
            "Explicit branch separation, documented transformations, missing-value handling, ranking provenance and clear separation of computational predictions from experimental claims.",
            f"The supplied tables contain {int((rankings['foldx_ddg'] < 0).sum()):,} candidates with negative FoldX ΔΔG and a mean best TM-score of {mean_tm:.3f} across the supplied structure-comparison summary.",
            "Predictions require experimental testing. Scores from different methods are model-dependent, and the public application does not establish improved enzyme performance in laboratory or industrial conditions.",
            "Downloadable filtered tables are provided in the app. Public workflow and results repositories provide additional context and provenance.",
        )
        c1, c2 = st.columns(2)
        c1.link_button("Results repository", RESULTS_REPO, icon="↗", use_container_width=True)
        c2.link_button("Workflow repository", WORKFLOW_REPO, icon="↗", use_container_width=True)


def render_afelele() -> None:
    phys = read_csv("afelele_physicochemical.csv")
    heavy = read_csv("afelele_heavy_metals.csv")
    classes = read_csv("afelele_proteobacteria_classes.csv")
    genera = read_csv("afelele_selected_genera.csv")
    species = read_csv("afelele_selected_species.csv")

    st.markdown("## Afelele Environmental & Metagenomic Assessment")
    st.markdown(
        '<div class="source-note">Surface-water concentrations are reported in mg/L and sediment concentrations in mg/kg. They are analysed in separate panels rather than treated as interchangeable measurements.</div>',
        unsafe_allow_html=True,
    )

    water_reads = int(classes["surface_water_reads"].sum())
    sediment_reads = int(classes["sediment_reads"].sum())
    water_dominant = classes.loc[classes["surface_water_percent"].idxmax(), "class"]
    sediment_dominant = classes.loc[classes["sediment_percent"].idxmax(), "class"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Surface-water reads", f"{water_reads:,}")
    m2.metric("Sediment reads", f"{sediment_reads:,}")
    m3.metric("Water-dominant class", water_dominant)
    m4.metric("Sediment-dominant class", sediment_dominant)

    overview, microbiome, chemistry, evidence_tab, documentation = st.tabs([
        "Overview", "Community analysis", "Environmental chemistry", "Field & laboratory evidence", "Methods & limitations"
    ])

    with overview:
        a, b = st.columns([0.95, 1.05], gap="large")
        with a:
            st.markdown(
                "The analysis joins environmental chemistry and metagenomic summaries to compare surface-water and sediment samples. "
                "The portfolio retains reported units, uncertainty values, detection status and source references while adding interactive comparative views."
            )
            tags([
                "Environmental microbiology", "Heavy metals", "Metagenomics", "Data extraction",
                "Comparative analysis", "Uncertainty visualisation", "Scientific reporting",
            ])
            st.markdown("### Analytical questions")
            st.markdown(
                """- How does Proteobacteria composition shift between sample matrices?
- Which selected genera are concentrated in one matrix or shared across both?
- What concentration patterns are visible within the water and sediment measurements?
- Which values are missing, not detected or not directly comparable?"""
            )
        with b:
            st.plotly_chart(afelele_class_shift(classes), use_container_width=True, config={"displaylogo": False}, key="afelele_overview_class_shift_chart")

    with microbiome:
        st.plotly_chart(afelele_class_shift(classes), use_container_width=True, config={"displaylogo": False}, key="afelele_community_class_shift_chart")
        st.caption("Connected points show the direction and magnitude of each class shift between surface water and sediment.")

        c1, c2 = st.columns([1.05, 0.95], gap="large")
        with c1:
            st.plotly_chart(afelele_genus_heatmap(genera), use_container_width=True, config={"displaylogo": False}, key="afelele_genus_heatmap_chart")
        with c2:
            genus_view = genera.copy()
            genus_view["total_reads"] = genus_view["surface_water_reads"].fillna(0) + genus_view["sediment_reads"].fillna(0)
            genus_view["sediment_share_percent"] = genus_view["sediment_reads"].fillna(0) / genus_view["total_reads"].replace(0, np.nan) * 100
            genus_view = genus_view.sort_values("total_reads", ascending=False)
            st.markdown("### Selected-genus analytical table")
            st.dataframe(
                genus_view[["genus", "surface_water_reads", "sediment_reads", "total_reads", "sediment_share_percent"]],
                hide_index=True, use_container_width=True,
                column_config={"sediment_share_percent": st.column_config.ProgressColumn("Sediment share", min_value=0, max_value=100, format="%.1f%%")},
            )
        st.markdown("### Selected species evidence")
        species_view = species.copy()
        species_view["surface_water_reads"] = species_view["surface_water_reads"].fillna(0)
        species_view["sediment_reads"] = species_view["sediment_reads"].fillna(0)
        species_view["matrix_pattern"] = np.select(
            [
                (species_view["surface_water_reads"] > 0) & (species_view["sediment_reads"] > 0),
                species_view["surface_water_reads"] > 0,
                species_view["sediment_reads"] > 0,
            ],
            ["Both matrices", "Surface water only", "Sediment only"],
            default="No reported reads",
        )
        st.dataframe(species_view, hide_index=True, use_container_width=True)
        st.download_button(
            "Download metagenomic summary tables",
            pd.concat([
                classes.assign(table="class composition"),
                genera.assign(table="selected genera"),
            ], ignore_index=True, sort=False).to_csv(index=False).encode(),
            "afelele_metagenomic_summaries.csv", "text/csv", icon="⬇️",
        )

    with chemistry:
        st.plotly_chart(afelele_metal_panels(heavy), use_container_width=True, config={"displaylogo": False}, key="afelele_heavy_metal_panels_chart")
        st.caption("Logarithmic x-axes reveal within-matrix concentration patterns across several orders of magnitude. The two panels retain their different units.")

        st.markdown("### Physicochemical parameter explorer")
        matrix = st.radio("Sample matrix", ["Surface water", "Sediment"], horizontal=True, key="afelele_matrix")
        if matrix == "Surface water":
            mean_col = "surface_water_mean"
            sd_col = "surface_water_standard_deviation"
            unit_col = "surface_water_unit"
        else:
            mean_col = "sediment_mean"
            sd_col = "sediment_standard_deviation"
            unit_col = "sediment_unit"

        available = phys[phys[mean_col].notna()].copy()
        available["relative_uncertainty_percent"] = available[sd_col] / available[mean_col].replace(0, np.nan) * 100
        selected_parameters = st.multiselect(
            "Parameters", available["parameter"].tolist(),
            default=available["parameter"].tolist(), key="afelele_parameters",
        )
        plot_data = available[available["parameter"].isin(selected_parameters)].copy()
        if not plot_data.empty:
            fig = px.scatter(
                plot_data, x=mean_col, y="parameter", size="relative_uncertainty_percent",
                hover_data={sd_col: True, unit_col: True, "relative_uncertainty_percent": ":.2f"},
                title=f"{matrix} physicochemical profile",
                labels={mean_col: "Reported mean", "parameter": ""},
                log_x=True, size_max=22,
            )
            fig.update_layout(height=max(430, 38 * len(plot_data)), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="afelele_physicochemical_chart")
        st.dataframe(phys, hide_index=True, use_container_width=True)
        c1, c2 = st.columns(2)
        c1.download_button("Download physicochemical data", phys.to_csv(index=False).encode(), "afelele_physicochemical.csv", "text/csv")
        c2.download_button("Download heavy-metal data", heavy.to_csv(index=False).encode(), "afelele_heavy_metals.csv", "text/csv")

    with evidence_tab:
        images = [
            ("afelele-pond.webp", None, "Environmental sampling location."),
            ("afelele-sterile.webp", None, "Sterile plating and inoculation activities."),
            ("afelele-microscopy.webp", None, "Microscopy-related laboratory work."),
        ]
        cols = st.columns(3)
        for col, (filename, folder, caption) in zip(cols, images):
            with col:
                show_image(filename, folder, caption)
        with st.expander("Source-generated and portfolio visuals"):
            c1, c2 = st.columns(2)
            with c1:
                show_image("afelele_heavy_metals_surface_water.png", "verified_results", "Surface-water concentration profile.")
            with c2:
                show_image("afelele_heavy_metals_sediment.png", "verified_results", "Sediment concentration profile.")

    with documentation:
        evidence_sections(
            "Compare physicochemical properties, heavy-metal content and Proteobacteria composition in surface-water and sediment samples.",
            "Participated in environmental sampling, laboratory processing, physicochemical and metal assessment, microbiological work, result interpretation and project documentation.",
            f"Structured portfolio extracts include {len(phys)} physicochemical parameters, {len(heavy)} heavy metals, {len(classes)} Proteobacteria classes and selected genus/species read-count evidence.",
            "Environmental sampling, physicochemical assessment, heavy-metal analysis, microbiological handling, metagenomic result interpretation, data restructuring and comparative visualisation.",
            "Original units are retained; surface water and sediment are not directly merged; not-detected values remain not detected; uncertainty values and source notes are preserved.",
            "The reported data show clear differences in Proteobacteria class composition and selected-genus read patterns between the two matrices, alongside distinct chemistry profiles within each matrix.",
            "The public extract represents reported samples and selected taxonomic summaries. It does not establish causation, clinical risk or environmental safety, and the displayed read counts are not a substitute for the complete sequence-analysis pipeline.",
            "The app includes structured CSV extracts, exact source notes, interactive analytical views and downloadable tables. Transformations are documented in DATA_PROVENANCE.md.",
        )


def render_rnaseq() -> None:
    evidence = read_csv("rnaseq_evidence_summary.csv")
    steps = read_csv("rnaseq_pipeline_steps.csv")

    metrics = evidence.set_index("metric")["value"].to_dict()
    st.markdown("## Reproducible RNA-seq Workflow")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Paired-end samples", int(metrics.get("paired_end_samples", 0)))
    m2.metric("Conditions", int(metrics.get("experimental_conditions", 0)))
    m3.metric("DESeq2 rows documented", f"{int(metrics.get('deseq2_result_rows', 0)):,}")
    m4.metric("Result fields", int(metrics.get("deseq2_result_fields", 0)))

    overview, pipeline, evidence_tab, reproducibility = st.tabs([
        "Project overview", "Pipeline", "Documented analysis evidence", "Reproducibility & limitations"
    ])

    with overview:
        a, b = st.columns([1.1, 0.9], gap="large")
        with a:
            st.markdown(
                "A six-sample, two-condition paired-end RNA-seq workflow covering quality control, trimming, alignment, gene-level quantification, differential-expression analysis and workflow orchestration."
            )
            tags(["FastQC", "Cutadapt", "STAR", "featureCounts", "DESeq2", "Snakemake", "Conda", "Linux"])
            workflow = download_path("Kamaldeen_RNAseq_Workflow_Template.zip")
            if workflow:
                with open(workflow, "rb") as file:
                    st.download_button(
                        "Download cleaned workflow template", file.read(), workflow.name,
                        "application/zip", icon="⬇️", use_container_width=True,
                    )
        with b:
            show_image("rnaseq_workflow_overview.png", "rnaseq", "Documented stages organised into a reproducible pipeline.")

    with pipeline:
        st.dataframe(steps, hide_index=True, use_container_width=True)
        show_image("rnaseq_evidence_metrics.png", "rnaseq", "Only values explicitly visible in the supplied report are summarised.")

    with evidence_tab:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            show_image("rnaseq_ma_plot_source.png", "rnaseq", "Source-generated MA plot from the documented DESeq2 analysis.")
        with c2:
            show_image("rnaseq_deseq2_result_excerpt.png", "rnaseq", "Documented DESeq2 result excerpt showing 1,378 rows and six fields.")
        with st.expander("Implementation evidence"):
            c1, c2 = st.columns(2)
            with c1:
                show_image("rnaseq_deseq2_script_source.png", "rnaseq", "DESeq2 command-line script evidence.")
            with c2:
                show_image("rnaseq_snakemake_source.png", "rnaseq", "Rule-based workflow evidence.")

    with reproducibility:
        evidence_sections(
            "Create a transparent paired-end RNA-seq workflow that coordinates quality control, trimming, alignment, quantification and differential-expression analysis.",
            "Configured the analysis environment, documented commands and outputs, implemented DESeq2 processing and organised the stages as a Snakemake workflow template.",
            "The supplied report documents six paired-end samples across two conditions, a 1,378-row DESeq2 result matrix, six standard result fields and a source-generated MA plot.",
            "FastQC, Cutadapt, STAR, featureCounts, DESeq2, Snakemake, Conda, Linux and reproducible file organisation.",
            "Explicit sample metadata, environment management, command documentation, intermediate outputs and rule dependencies support repeatability and troubleshooting.",
            "The public evidence demonstrates successful workflow execution and the documented DESeq2 output structure. No additional gene-level findings were generated without the full source tables.",
            "Raw FASTQ files, reference files and the complete count/result matrices were not supplied in the portfolio bundle. No new significant-gene counts or biological conclusions are inferred.",
            "A cleaned workflow template is downloadable. The source-generated MA plot and implementation excerpts are shown separately from the reusable template.",
        )


def render_breast_cancer() -> None:
    data = read_csv("breast_cancer_cleaned_568.csv")
    feature_summary = read_csv("breast_cancer_feature_summary.csv")
    quality = read_csv("breast_cancer_quality_summary.csv")

    malignant_count = int((data["Diagnosis"] == "Malignant").sum())
    missing_area = int(data["Area Mean"].isna().sum())
    pca, explained = breast_cancer_pca(data)

    st.markdown("## Breast Cancer Diagnostic Data Analysis")
    st.warning("This is educational, descriptive analysis. It is not a diagnostic model or patient-level risk tool.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Uploaded records", f"{len(data):,}")
    m2.metric("Malignant diagnoses", f"{malignant_count:,}")
    m3.metric("Malignant share", f"{malignant_count / len(data):.1%}")
    m4.metric("Missing Area Mean", missing_area)

    overview, multivariate, distributions, relationships, audit = st.tabs([
        "Overview", "Multivariate analysis", "Feature distributions", "Relationships", "Audit & limitations"
    ])

    with overview:
        a, b = st.columns([0.95, 1.05], gap="large")
        with a:
            st.markdown(
                "The original Excel dashboard was audited and rebuilt around the 568 records actually supplied. "
                "Incorrect KPI logic was corrected, one missing value was retained transparently and the former clinical-sounding risk field was reframed as a descriptive Radius Band."
            )
            tags([
                "Microsoft Excel", "Data cleaning", "Exploratory analysis", "PCA",
                "Correlation analysis", "Dashboard redesign", "Healthcare data",
            ])
            workbook = download_path("Kamaldeen_Breast_Cancer_Data_Analysis_Cleaned.xlsx")
            if workbook:
                with open(workbook, "rb") as file:
                    st.download_button(
                        "Download cleaned Excel workbook", file.read(), workbook.name,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        icon="⬇️", use_container_width=True,
                    )
            st.link_button(
                "View Excel project repository", "https://github.com/Kanmi77/EXCEL_Data_Analysis",
                icon="↗", use_container_width=True,
            )
            st.markdown("### Data-quality corrections")
            st.markdown(
                """- Record count corrected from 569 to 568.
- The original average-radius KPI was identified as a sum.
- One missing Area Mean value remains missing in the cleaned dataset.
- Radius Band is explicitly descriptive and not a validated clinical score."""
            )
        with b:
            fig = px.scatter(
                pca, x="PC1", y="PC2", color="Diagnosis", hover_name="Patient ID",
                hover_data={"Radius Mean": ":.3f", "Area Mean": ":.1f"},
                title=f"Principal-component view · PC1 {explained[0]:.1%}, PC2 {explained[1]:.1%}",
                labels={"PC1": f"PC1 ({explained[0]:.1%})", "PC2": f"PC2 ({explained[1]:.1%})"},
                opacity=0.72,
            )
            fig.update_traces(marker={"size": 8})
            fig.update_layout(height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="breast_overview_pca_chart")

    with multivariate:
        diagnoses = st.multiselect(
            "Diagnosis groups", sorted(pca["Diagnosis"].unique()),
            default=sorted(pca["Diagnosis"].unique()), key="bc_pca_diagnosis",
        )
        pca_filtered = pca[pca["Diagnosis"].isin(diagnoses)]
        fig = px.scatter(
            pca_filtered, x="PC1", y="PC2", color="Diagnosis", hover_name="Patient ID",
            hover_data={"Radius Mean": ":.3f", "Area Mean": ":.1f"},
            title=f"PCA of standardised numeric measurements · cumulative variance {(explained[0] + explained[1]):.1%}",
            labels={"PC1": f"PC1 ({explained[0]:.1%})", "PC2": f"PC2 ({explained[1]:.1%})"},
            opacity=0.72,
        )
        fig.update_traces(marker={"size": 8})
        fig.update_layout(height=600, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="breast_multivariate_pca_chart")
        st.caption("All numeric features are standardised before PCA. The single missing Area Mean value is median-imputed only for this calculation.")

        numeric_columns = [
            column for column in data.select_dtypes(include=[np.number]).columns
            if column != "Patient ID"
        ]
        correlation = data[numeric_columns].corr()
        selected_corr = st.multiselect(
            "Features in correlation heatmap", numeric_columns,
            default=[
                "Radius Mean", "Perimeter Mean", "Area Mean", "Compactness Mean",
                "Concavity Mean", "Concave Points Mean", "Area Worst",
            ], key="bc_corr_features",
        )
        if len(selected_corr) >= 2:
            corr = correlation.loc[selected_corr, selected_corr]
            fig_corr = go.Figure(go.Heatmap(
                z=corr.to_numpy(), x=corr.columns, y=corr.index, zmin=-1, zmax=1, zmid=0,
                hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
                colorbar={"title": "Pearson r"},
            ))
            fig_corr.update_layout(
                title="Selectable feature-correlation matrix", height=max(520, 42 * len(selected_corr)),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_corr, use_container_width=True, config={"displaylogo": False}, key="breast_correlation_heatmap_chart")

    with distributions:
        numeric_columns = [
            column for column in data.select_dtypes(include=[np.number]).columns
            if column != "Patient ID"
        ]
        selected_feature = st.selectbox("Feature", numeric_columns, index=numeric_columns.index("Concavity Mean"), key="bc_feature")
        plot_type = st.radio("Distribution view", ["Violin", "Box", "Histogram"], horizontal=True, key="bc_distribution_type")
        if plot_type == "Violin":
            fig = px.violin(
                data, x="Diagnosis", y=selected_feature, color="Diagnosis", box=True, points="outliers",
                title=f"{selected_feature} distribution by diagnosis",
            )
        elif plot_type == "Box":
            fig = px.box(
                data, x="Diagnosis", y=selected_feature, color="Diagnosis", points="outliers",
                title=f"{selected_feature} distribution by diagnosis",
            )
        else:
            fig = px.histogram(
                data, x=selected_feature, color="Diagnosis", marginal="box", barmode="overlay", opacity=0.65,
                title=f"{selected_feature} distribution by diagnosis",
            )
        fig.update_layout(height=560, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="breast_distribution_chart")

        st.markdown("### Group-level feature summary")
        display = feature_summary[["Feature", "Benign Mean", "Malignant Mean", "Malignant / Benign Ratio"]].copy()
        st.dataframe(
            display, hide_index=True, use_container_width=True,
            column_config={
                "Malignant / Benign Ratio": st.column_config.NumberColumn(
                    "Malignant / Benign", format="%.2f×"
                )
            },
        )

    with relationships:
        numeric_columns = [
            column for column in data.select_dtypes(include=[np.number]).columns
            if column != "Patient ID"
        ]
        c1, c2 = st.columns(2)
        x_feature = c1.selectbox("X feature", numeric_columns, index=numeric_columns.index("Radius Mean"), key="bc_x")
        y_feature = c2.selectbox("Y feature", numeric_columns, index=numeric_columns.index("Area Mean"), key="bc_y")
        c3, c4 = st.columns(2)
        selected_diagnoses = c3.multiselect(
            "Diagnosis", sorted(data["Diagnosis"].unique()),
            default=sorted(data["Diagnosis"].unique()), key="bc_rel_diag",
        )
        selected_bands = c4.multiselect(
            "Radius Band", ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"], key="bc_rel_band",
        )
        filtered = data[data["Diagnosis"].isin(selected_diagnoses) & data["Radius Band"].isin(selected_bands)].copy()
        fig = px.scatter(
            filtered, x=x_feature, y=y_feature, color="Diagnosis", symbol="Radius Band",
            hover_data=["Patient ID", "Perimeter Mean", "Concavity Mean"],
            marginal_x="histogram", marginal_y="box", opacity=0.68,
            title=f"{x_feature} versus {y_feature}",
        )
        fig.update_layout(height=650, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False}, key="breast_relationship_chart")
        st.caption("Records with a missing value in either selected feature are excluded from this relationship view.")
        st.download_button(
            "Download cleaned CSV", data.to_csv(index=False).encode(),
            "breast_cancer_cleaned_568.csv", "text/csv", icon="⬇️",
        )

    with audit:
        st.dataframe(quality, hide_index=True, use_container_width=True)
        evidence_sections(
            "Correct errors in the original dashboard and present an accurate, transparent exploratory analysis of the supplied diagnostic dataset.",
            "Audited record counts and fields; preserved missingness; corrected KPI logic; rebuilt the Excel dashboard; generated multivariate, distributional and relationship views.",
            f"The uploaded workbook contains {len(data):,} records: {int((data['Diagnosis']=='Benign').sum()):,} benign and {malignant_count:,} malignant diagnoses, with one missing Area Mean value.",
            "Microsoft Excel, data cleaning, descriptive statistics, PCA, grouped feature comparison, correlation analysis and interactive Plotly visualisation.",
            "Duplicate-ID checks, missing-value audit, corrected aggregation logic, transparent PCA-only imputation and explicit definition of descriptive Radius Bands.",
            "The rebuilt dashboard reports 568 records and a malignant share of 37.1%. Multivariate and group comparisons are descriptive and restricted to the supplied data.",
            "The project does not provide diagnosis, prognosis, treatment recommendations or a validated clinical risk score. No classifier is presented.",
            "The cleaned workbook, CSV and visual evidence are downloadable. Cleaning decisions are documented in the workbook's Data Quality and Methodology sheets.",
        )


def render_operational() -> None:
    st.markdown("## Operational Data Analysis & Decision Support")
    st.info("Employer datasets and numerical business results are not published because they are confidential.")

    a, b = st.columns(2, gap="large")
    with a:
        project_card(
            "Operational analytics",
            "Data preparation and quality",
            "Cleaned and structured operational datasets, investigated incomplete or inconsistent records and prepared analysis-ready inputs.",
            "Professional experience record; no confidential raw data is exposed.",
        )
    with b:
        project_card(
            "Decision support",
            "Analysis and communication",
            "Applied Python, R, SQL and statistical methods to examine patterns and trends, then translated findings into reports, presentations and visual outputs.",
            "Methods and contribution are documented without inventing performance metrics.",
        )

    evidence_sections(
        "Convert operational data into reliable analysis and clear information for business decision-making.",
        "Cleaned and interpreted datasets; applied statistical and machine-learning methods; prepared visual outputs and communicated findings to stakeholders.",
        "The underlying employer datasets are confidential and are therefore not included in the public portfolio.",
        "Python, R, SQL, data cleaning, exploratory analysis, trend analysis, forecasting support, visualisation and reporting.",
        "Structured data-entry checks, missing and inconsistent record review, documented transformations and careful explanation of analytical limitations.",
        "The work supported decision-making through analytical reports and presentations. No numerical employer outcomes are stated because supporting public evidence is unavailable.",
        "Confidentiality prevents publication of source data, dashboards and business-sensitive metrics. The page therefore functions as a scoped professional case study rather than a reproducible public analysis.",
        "Public GitHub projects demonstrate adjacent technical foundations, while this case study documents the professional workflow and responsibilities only.",
    )
    st.link_button("View data-project repositories", GITHUB, icon="↗", use_container_width=True)


def render_laboratory() -> None:
    st.markdown("## Laboratory Quality & Microbiology Practice")
    st.markdown(
        "A selected evidence gallery covering pharmaceutical quality-control support, clinical laboratory exposure, environmental microbiology and analytical-laboratory practice."
    )

    tabs = st.tabs(["Pharmaceutical QC", "Clinical laboratory", "Research laboratory", "Environmental microbiology", "Scope & methods"])
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            show_image("mopsin.webp", None, "Pharmaceutical laboratory and quality-control practice.")
        with c2:
            show_image("mopsin-control.webp", None, "Water-quality and control-related laboratory activities.")
        st.markdown("Supported sample preparation, QC testing, SOP-based documentation, hygiene requirements, organised records and traceable laboratory operations.")

    with tabs[1]:
        cols = st.columns(3)
        clinical_images = ["dr_hammond_1.jpg", "dr_hammond_2.jpg", "dr_hammond_3.jpg"]
        for col, filename in zip(cols, clinical_images):
            with col:
                show_image(filename, None, "Clinical microscopy and laboratory practice at Dr. Hammond Clinic.")
        st.markdown("Experience included sample handling, clinical-testing support, microscopy, infection-prevention practices and accurate documentation.")

    with tabs[2]:
        evidence = [
            ("uilorin-gc.webp", "Analytical-instrument exposure in the central research laboratory."),
            ("uilorin-sample.webp", "Structured sample preparation and handling."),
            ("uilorin-ultrasonic.webp", "Laboratory equipment and sample-processing exposure."),
            ("agbaje-team.webp", "Research-team experience in the bio-nanotechnology laboratory."),
        ]
        cols = st.columns(2)
        for idx, (filename, caption) in enumerate(evidence):
            with cols[idx % 2]:
                show_image(filename, None, caption)

    with tabs[3]:
        cols = st.columns(3)
        environmental = [
            ("afelele-pond.webp", "Environmental sampling site."),
            ("afelele-sterile.webp", "Sterile plating and inoculation work."),
            ("afelele-microscopy.webp", "Microscopy-related environmental microbiology work."),
        ]
        for col, (filename, caption) in zip(cols, environmental):
            with col:
                show_image(filename, None, caption)

    with tabs[4]:
        evidence_sections(
            "Support reliable laboratory work across pharmaceutical QC, clinical testing, microbiological research and environmental sample analysis.",
            "Performed or supported sample preparation, microscopy, microbiological assays, laboratory documentation, equipment use, hygiene controls and research record keeping within the scope of each placement.",
            "Public evidence consists of professional photographs and experience records. Patient information, restricted identifiers and confidential laboratory documents are excluded.",
            "Aseptic practice, sample handling, microscopy, PCR and gel-electrophoresis support, microbiological assays, analytical-instrument exposure, SOP compliance and laboratory safety.",
            "PPE, contamination-control practices, accurate records, organised work areas, sample traceability and careful adherence to assigned protocols.",
            "The evidence demonstrates breadth of laboratory exposure and quality-conscious practice. It does not claim independent mastery of every photographed instrument or regulated release authority beyond documented responsibilities.",
            "Photographs cannot by themselves prove analytical competency level. Captions therefore describe only visible or previously documented activities, and no patient or confidential information is shown.",
            "The portfolio combines scoped captions with experience dates and downloadable CV evidence. Additional certificates or protocols can be added when approved for public use.",
        )


header(
    "Evidence-based professional work",
    "Project Explorer",
    "Every project has a dedicated analytical or evidence view. Use the project tabs below to move directly between data, methods, quality controls, results, downloads and limitations.",
)

st.markdown("## Portfolio coverage")
coverage = pd.DataFrame([
    {"Project": "Xylanase Thermostability", "Public data": "Yes", "Interactive analysis": "Candidate landscape, parallel coordinates, MD heatmap", "Downloads": "Filtered candidates", "Evidence type": "Computational research"},
    {"Project": "Afelele Environmental & Metagenomic", "Public data": "Yes", "Interactive analysis": "Community shift, genus heatmap, chemistry panels", "Downloads": "Chemistry and metagenomic tables", "Evidence type": "Environmental microbiology"},
    {"Project": "RNA-seq Workflow", "Public data": "Partial", "Interactive analysis": "Pipeline and documented execution evidence", "Downloads": "Workflow template", "Evidence type": "Reproducible bioinformatics"},
    {"Project": "Breast Cancer Data Analysis", "Public data": "Yes", "Interactive analysis": "PCA, distributions, correlations, relationship explorer", "Downloads": "Cleaned CSV and Excel workbook", "Evidence type": "Healthcare analytics"},
    {"Project": "Operational Data Analysis", "Public data": "No — confidential", "Interactive analysis": "Scoped professional case study", "Downloads": "Public repositories", "Evidence type": "Professional analytics"},
    {"Project": "Laboratory Quality & Microbiology", "Public data": "Not applicable", "Interactive analysis": "Evidence gallery by practice area", "Downloads": "CV evidence", "Evidence type": "Laboratory practice"},
])
st.dataframe(coverage, hide_index=True, use_container_width=True)

st.markdown("## Project directory")
project_summaries = [
    ("Computational biology", "Xylanase Thermostability Research", "Candidate ranking, evidence integration, structural comparison and MD response."),
    ("Environmental microbiology", "Afelele Environmental & Metagenomic Assessment", "Community shifts, genus fingerprints, heavy metals and physicochemical evidence."),
    ("Transcriptomics", "Reproducible RNA-seq Workflow", "Six-sample pipeline evidence, implementation records and workflow template."),
    ("Healthcare analytics", "Breast Cancer Diagnostic Data Analysis", "PCA, distributions, correlations, relationship exploration and data-quality audit."),
    ("Professional analytics", "Operational Data Analysis & Decision Support", "Confidentiality-aware evidence of data preparation, analysis and stakeholder reporting."),
    ("Laboratory practice", "Laboratory Quality & Microbiology Practice", "Clinical, pharmaceutical, research and environmental laboratory evidence."),
]
for start in range(0, len(project_summaries), 3):
    cols = st.columns(3, gap="large")
    for col, (kicker, title, body) in zip(cols, project_summaries[start:start + 3]):
        with col:
            project_card(kicker, title, body, "Detailed access is available from the selector below.")

st.markdown("## Detailed project access")
selected = st.selectbox(
    "Choose a project to open", PROJECTS, index=None,
    placeholder="Select any project — no project is prioritised by default",
    key="project_detail_selection",
)
if selected is None:
    st.info("Select a project above to open its interactive analysis, methods, verified results, downloads and limitations.")
else:
    st.divider()
    renderers = {
        PROJECTS[0]: render_xylanase,
        PROJECTS[1]: render_afelele,
        PROJECTS[2]: render_rnaseq,
        PROJECTS[3]: render_breast_cancer,
        PROJECTS[4]: render_operational,
        PROJECTS[5]: render_laboratory,
    }
    renderers[selected]()
