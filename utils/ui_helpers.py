from pathlib import Path

import streamlit as st


APP_ROOT = Path(__file__).resolve().parents[1]
ARCWISE_LOGO_PATH = APP_ROOT / "assets" / "arcwise_logo.png"


def get_arcwise_logo_path() -> Path | None:
    return ARCWISE_LOGO_PATH if ARCWISE_LOGO_PATH.exists() else None


def render_cutting_mode_sidebar():
    st.session_state["cut_mode"] = "Standard"


def render_arcwise_theme():
    st.markdown(
        """
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(23, 127, 255, 0.18), transparent 34rem),
        linear-gradient(180deg, #060b12 0%, #08111b 48%, #070a0f 100%);
    color: #e7f1fb;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.35rem;
    padding-bottom: 1.2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] strong {
    color: #edf7ff;
}

p, li, label, [data-testid="stMarkdownContainer"] {
    color: #b8c8d9;
}

hr {
    border-color: rgba(83, 167, 255, 0.16);
}

.arcwise-page-head {
    border: 1px solid rgba(83, 167, 255, 0.18);
    border-radius: 8px;
    padding: 19px 20px 17px;
    background:
        radial-gradient(circle at center top, rgba(40, 150, 255, 0.16), transparent 15rem),
        linear-gradient(180deg, rgba(12, 28, 45, 0.94), rgba(6, 13, 22, 0.96));
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28), inset 0 -1px 0 rgba(82, 169, 255, 0.12);
    margin-bottom: 0.85rem;
    overflow: hidden;
    position: relative;
}

.arcwise-page-head:after {
    background: linear-gradient(90deg, transparent, rgba(86, 186, 255, 0.54), transparent);
    bottom: 0;
    content: "";
    height: 1px;
    left: 9%;
    position: absolute;
    right: 9%;
}

.arcwise-kicker {
    color: #88b8e7;
    font-size: 0.74rem;
    font-weight: 760;
    letter-spacing: 0.13em;
    line-height: 1.35;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
}

.arcwise-page-title {
    color: #f2f8ff;
    font-size: clamp(1.65rem, 2.5vw, 2.22rem);
    font-weight: 820;
    letter-spacing: 0;
    line-height: 1.08;
    margin-bottom: 0.42rem;
}

.arcwise-page-subtitle {
    color: #a9bdd2;
    font-size: 0.94rem;
    line-height: 1.45;
    max-width: 850px;
}

.arcwise-panel {
    border: 1px solid rgba(88, 173, 255, 0.16);
    border-radius: 8px;
    padding: 14px 15px;
    background: linear-gradient(180deg, rgba(18, 38, 58, 0.72), rgba(7, 14, 23, 0.88));
    box-shadow: 0 12px 32px rgba(0,0,0,0.22), 0 0 0 1px rgba(255,255,255,0.022) inset;
}

.arcwise-note {
    border: 1px solid rgba(88, 173, 255, 0.16);
    border-radius: 8px;
    padding: 12px 14px;
    background: rgba(40, 150, 255, 0.075);
    color: #c7d8e8;
    font-size: 0.91rem;
    line-height: 1.42;
    margin-bottom: 0.75rem;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(88, 173, 255, 0.16);
    border-radius: 8px;
    padding: 0.72rem 0.82rem;
    background: linear-gradient(180deg, rgba(20, 43, 63, 0.76), rgba(8, 16, 25, 0.92));
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}

[data-testid="stMetric"] label,
[data-testid="stMetricLabel"] {
    color: #95adc4;
}

[data-testid="stMetricValue"] {
    color: #edf7ff;
}

div[data-testid="stTabs"] button {
    color: #a9bdd2;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #edf7ff;
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: #46a9ff;
}

div[data-testid="stExpander"] {
    border: 1px solid rgba(88, 173, 255, 0.16);
    border-radius: 8px;
    background: linear-gradient(180deg, rgba(14, 31, 48, 0.76), rgba(7, 14, 23, 0.88));
}

div[data-testid="stExpander"] summary {
    color: #e4f2ff;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid rgba(88, 173, 255, 0.14);
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stCodeBlock"] pre,
pre {
    border: 1px solid rgba(88, 173, 255, 0.18);
    border-radius: 8px;
    background: #07111c !important;
    color: #d7ecff !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="base-input"],
input,
textarea {
    background-color: #0d1a28 !important;
    border-color: rgba(88, 173, 255, 0.22) !important;
    color: #edf7ff !important;
}

div[data-baseweb="select"] svg {
    color: #91caff;
}

div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(180deg, rgba(33, 104, 171, 0.35), rgba(10, 25, 40, 0.92));
    border-color: rgba(83, 167, 255, 0.28);
    border-radius: 8px;
    color: #dceeff;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: rgba(89, 184, 255, 0.55);
    color: #ffffff;
}

[data-testid="stAlert"] {
    border-radius: 8px;
    border: 1px solid rgba(88, 173, 255, 0.16);
    background: rgba(15, 31, 48, 0.88);
    color: #e7f1fb;
}

@media (max-width: 640px) {
    .block-container {
        padding-left: 0.85rem;
        padding-right: 0.85rem;
        padding-top: 0.9rem;
    }

    .arcwise-page-head {
        padding: 16px 15px 14px;
    }

    .arcwise-page-title {
        font-size: 1.55rem;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, kicker: str = "ArcWise Workbench"):
    st.markdown(
        f"""
<div class="arcwise-page-head">
    <div class="arcwise-kicker">{kicker}</div>
    <div class="arcwise-page-title">{title}</div>
    <div class="arcwise-page-subtitle">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_sidebar_nav(current_page: str):
    render_arcwise_theme()
    st.markdown(
        """
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111d 0%, #0a121b 52%, #070b10 100%);
    border-right: 1px solid rgba(82, 169, 255, 0.14);
}

[data-testid="stSidebar"] [data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin: 0.2rem 0 0.8rem;
}

[data-testid="stSidebar"] .stPageLink a {
    border-radius: 8px;
    padding: 0.45rem 0.55rem;
}

[data-testid="stSidebar"] .stPageLink a:hover {
    background: rgba(48, 145, 255, 0.10);
}

.arcwise-sidebar-title {
    color: #eef7ff;
    font-size: 1.28rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-align: center;
    margin: 0.1rem 0 0.8rem;
}

.arcwise-sidebar-section {
    color: #8fb4d9;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.14em;
    margin: 0.65rem 0 0.45rem;
    text-transform: uppercase;
}
</style>
""",
        unsafe_allow_html=True,
    )

    logo_path = get_arcwise_logo_path()
    if logo_path:
        st.sidebar.image(str(logo_path), width=150)
    else:
        st.sidebar.markdown('<div class="arcwise-sidebar-title">ArcWise</div>', unsafe_allow_html=True)

    st.sidebar.markdown('<div class="arcwise-sidebar-section">Workbench</div>', unsafe_allow_html=True)
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Speeds_Feeds.py", label="Speeds & Feeds")
    st.sidebar.page_link("pages/2_Threads.py", label="Threads")
    st.sidebar.page_link("pages/3_Calculators.py", label="Math Workbench")
    st.sidebar.page_link("pages/6_G_M_Codes.py", label="G/M Codes & References")
