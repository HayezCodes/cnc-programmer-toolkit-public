from pathlib import Path

import streamlit as st


APP_ROOT = Path(__file__).resolve().parents[1]
CUTWISE_LOGO_PATH = APP_ROOT / "assets" / "cutwise_logo.png"


def get_cutwise_logo_path() -> Path | None:
    return CUTWISE_LOGO_PATH if CUTWISE_LOGO_PATH.exists() else None


def render_cutting_mode_sidebar():
    st.session_state["cut_mode"] = "Standard"


def render_sidebar_nav(current_page: str):
    logo_path = get_cutwise_logo_path()
    if logo_path:
        st.sidebar.image(str(logo_path), width=170)
    else:
        st.sidebar.title("CutWise")

    st.sidebar.markdown("### Workbench")
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Speeds_Feeds.py", label="Speeds & Feeds")
    st.sidebar.page_link("pages/2_Threads.py", label="Threads")
    st.sidebar.page_link("pages/3_Calculators.py", label="Math Workbench")
    st.sidebar.page_link("pages/6_G_M_Codes.py", label="G/M Codes & References")
