from __future__ import annotations

from pathlib import Path
from typing import Iterable

import streamlit as st

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
IMAGES = ASSETS / "images"
DOCS = ASSETS / "docs"
DATA = ROOT / "data"

EMAIL = "Sunkanmikamal.edu@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/kamaldeenbada"
GITHUB = "https://github.com/Kanmi77"
RESULTS_REPO = "https://github.com/Kanmi77/xylanase-thermostability-results"
WORKFLOW_REPO = "https://github.com/Kanmi77/xylanase-repo"


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
          --ink: #13231d;
          --muted: #5d6c66;
          --forest: #123f31;
          --forest-2: #1f604c;
          --sage: #dbe8e1;
          --cream: #f7f4ed;
          --paper: #fffef9;
          --gold: #a47b35;
          --line: rgba(18,63,49,.15);
        }
        html, body, [class*="css"]  { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
        .stApp { background: linear-gradient(180deg, #fbfaf6 0%, #f7f4ed 100%); color: var(--ink); }
        header[data-testid="stHeader"] { background: rgba(251,250,246,.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }
        [data-testid="stAppViewContainer"] > .main { background: transparent; }
        .block-container { max-width: 1180px; padding-top: 2.1rem; padding-bottom: 4rem; }
        h1, h2, h3 { color: var(--ink); letter-spacing: -.025em; }
        h1 { font-size: clamp(2.55rem, 5.5vw, 5.25rem) !important; line-height: .98 !important; font-weight: 760 !important; }
        h2 { font-size: clamp(1.8rem, 3vw, 2.65rem) !important; margin-top: 1.4rem !important; }
        h3 { font-size: 1.2rem !important; }
        p, li { color: var(--muted); line-height: 1.72; }
        a { color: var(--forest-2); text-decoration: none; }
        a:hover { color: var(--gold); }
        .eyebrow { text-transform: uppercase; letter-spacing: .17em; font-size: .72rem; color: var(--gold); font-weight: 800; margin-bottom: .65rem; }
        .hero-copy { font-size: clamp(1.08rem, 1.65vw, 1.32rem); max-width: 760px; color: var(--muted); line-height: 1.7; }
        .hero-role { color: var(--forest-2); font-size: clamp(1.15rem, 2vw, 1.55rem); font-weight: 700; margin: .5rem 0 1rem; }
        .availability { display: inline-flex; align-items: center; gap: .55rem; padding: .48rem .8rem; background: #eaf3ee; border: 1px solid #cadfd3; border-radius: 999px; color: var(--forest); font-size: .82rem; font-weight: 700; }
        .availability:before { content: ""; width: .55rem; height: .55rem; background: #3a936b; border-radius: 50%; box-shadow: 0 0 0 4px rgba(58,147,107,.12); }
        .card { background: rgba(255,254,249,.94); border: 1px solid var(--line); border-radius: 18px; padding: 1.35rem 1.35rem 1.2rem; box-shadow: 0 14px 35px rgba(24,47,38,.055); height: 100%; }
        .card h3 { margin-top: .1rem; }
        .card p:last-child { margin-bottom: .1rem; }
        .metric-card { background: var(--forest); color: white; border-radius: 16px; padding: 1.15rem 1.2rem; min-height: 122px; box-shadow: 0 14px 35px rgba(18,63,49,.17); }
        .metric-value { font-size: 2.05rem; font-weight: 800; letter-spacing: -.04em; color: white; }
        .metric-label { font-size: .82rem; color: rgba(255,255,255,.74); line-height: 1.35; }
        .tag { display:inline-block; padding:.32rem .58rem; margin:.15rem .2rem .15rem 0; border:1px solid #c9dacf; background:#eef5f1; color:var(--forest); border-radius:999px; font-size:.76rem; font-weight:650; }
        .section-kicker { color: var(--gold); font-weight: 800; letter-spacing: .13em; text-transform: uppercase; font-size: .72rem; }
        .section-lead { max-width: 800px; font-size: 1.05rem; }
        .project-card { position: relative; overflow: hidden; }
        .project-card:before { content:""; position:absolute; left:0; top:0; bottom:0; width:5px; background:linear-gradient(180deg,var(--forest-2),var(--gold)); }
        .timeline { border-left: 2px solid #cbdcd3; padding-left: 1.35rem; margin-left: .35rem; }
        .timeline-item { position: relative; padding: 0 0 1.35rem .45rem; }
        .timeline-item:before { content:""; position:absolute; left:-1.82rem; top:.32rem; width:.72rem; height:.72rem; border-radius:50%; background:var(--forest-2); border:3px solid var(--cream); box-shadow:0 0 0 1px var(--forest-2); }
        .timeline-date { color: var(--gold); font-weight: 800; font-size: .78rem; letter-spacing: .04em; }
        .timeline-role { color:var(--ink); font-size:1.05rem; font-weight:760; }
        .timeline-org { color:var(--forest-2); font-weight:650; }
        .photo-caption { font-size:.78rem; color:var(--muted); margin-top:.4rem; }
        .source-note { font-size:.78rem; color:#718079; border-left:3px solid #c9dacf; padding-left:.8rem; }
        .footer { margin-top: 4rem; padding-top: 1.25rem; border-top: 1px solid var(--line); color:#74827c; font-size:.82rem; display:flex; justify-content:space-between; flex-wrap:wrap; gap:.5rem; }
        div[data-testid="stMetric"] { background: var(--paper); border:1px solid var(--line); padding: .8rem 1rem; border-radius:14px; }
        div[data-testid="stMetricLabel"] { color: var(--muted); }
        div[data-testid="stMetricValue"] { color: var(--forest); }
        div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; }
        div[data-testid="stExpander"] { background:rgba(255,254,249,.75); border:1px solid var(--line); border-radius:14px; }
        .stButton > button, .stDownloadButton > button, .stLinkButton > a {
          border-radius: 999px !important; font-weight: 760 !important; border: 1px solid var(--forest) !important;
          transition: all .18s ease; min-height: 2.75rem;
        }
        .stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover { transform: translateY(-1px); box-shadow: 0 9px 24px rgba(18,63,49,.14); }
        [data-testid="stImage"] img { border-radius: 16px; }
        [data-testid="stFileUploader"] { background: var(--paper); border-radius:16px; padding:.4rem; }
        @media (max-width: 700px) {
          .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1.4rem; }
          h1 { font-size: 2.65rem !important; }
          .footer { display:block; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header(eyebrow: str, title: str, lead: str | None = None) -> None:
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if lead:
        st.markdown(f'<p class="section-lead">{lead}</p>', unsafe_allow_html=True)


def tags(items: Iterable[str]) -> None:
    html = "".join(f'<span class="tag">{item}</span>' for item in items)
    st.markdown(html, unsafe_allow_html=True)


def card(title: str, body: str, kicker: str | None = None) -> None:
    kicker_html = f'<div class="section-kicker">{kicker}</div>' if kicker else ""
    st.markdown(
        f'<div class="card">{kicker_html}<h3>{title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def metric_card(value: str, label: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def project_card(kicker: str, title: str, body: str, evidence: str) -> None:
    st.markdown(
        f"""
        <div class="card project-card">
          <div class="section-kicker">{kicker}</div>
          <h3>{title}</h3>
          <p>{body}</p>
          <p><strong style="color:#123f31">Evidence:</strong> {evidence}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def timeline_item(date: str, role: str, organisation: str, contribution: str) -> None:
    st.markdown(
        f"""
        <div class="timeline-item">
          <div class="timeline-date">{date}</div>
          <div class="timeline-role">{role}</div>
          <div class="timeline-org">{organisation}</div>
          <p>{contribution}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        f"""
        <div class="footer">
          <span>© 2026 Kamaldeen Olasunkanmi Bada · Bavaria, Germany</span>
          <span><a href="mailto:{EMAIL}">Email</a> · <a href="{LINKEDIN}" target="_blank">LinkedIn</a> · <a href="{GITHUB}" target="_blank">GitHub</a></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Robust file discovery
# ---------------------------------------------------------------------------
# GitHub's browser uploader can flatten folders when individual files are
# selected. These helpers prefer the intended folder structure, but also find
# files placed at the repository root or inside an extra nested folder.

from functools import lru_cache


@lru_cache(maxsize=None)
def locate_file(filename: str, preferred_folder: str | None = None) -> Path:
    candidates: list[Path] = []
    if preferred_folder:
        candidates.append(ROOT / preferred_folder / filename)
    candidates.append(ROOT / filename)

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    matches = [path for path in ROOT.rglob(filename) if path.is_file()]
    if matches:
        # Prefer the shortest relative path to avoid selecting files in caches.
        return sorted(matches, key=lambda p: len(p.relative_to(ROOT).parts))[0]

    expected = f"{preferred_folder}/{filename}" if preferred_folder else filename
    raise FileNotFoundError(
        f"Required portfolio file was not found: {expected}. "
        "Upload the complete extracted package, including the data and assets folders."
    )


def data_file(filename: str) -> Path:
    return locate_file(filename, "data")


def image_file(filename: str, subfolder: str | None = None) -> Path:
    preferred = "assets/images" if not subfolder else f"assets/images/{subfolder}"
    return locate_file(filename, preferred)


def document_file(filename: str) -> Path:
    return locate_file(filename, "assets/docs")


def download_file(filename: str) -> Path:
    return locate_file(filename, "assets/downloads")


def code_file(filename: str) -> Path:
    return locate_file(filename, "assets/code")


def show_missing_file_error(error: FileNotFoundError) -> None:
    st.error(str(error))
    st.info(
        "Expected repository structure: streamlit_app.py, portfolio.py, requirements.txt, "
        "pages/, data/, assets/ and .streamlit/ at the repository root."
    )
    st.stop()
