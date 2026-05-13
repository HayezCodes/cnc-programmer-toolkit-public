from pathlib import Path

import streamlit as st


APP_ROOT = Path(__file__).resolve().parents[1]
ARCWISE_LOGO_PATH = APP_ROOT / "assets" / "arcwise_logo.png"


def get_arcwise_logo_path() -> Path | None:
    return ARCWISE_LOGO_PATH if ARCWISE_LOGO_PATH.exists() else None


def render_cutting_mode_sidebar():
    st.session_state["cut_mode"] = "Standard"


def render_sidebar_nav(current_page: str):
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
