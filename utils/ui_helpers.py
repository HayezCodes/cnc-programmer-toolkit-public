import streamlit as st


def render_cutting_mode_sidebar():
    st.session_state["cut_mode"] = "Standard"


def render_sidebar_nav(current_page: str):
    st.sidebar.title("CNC Toolkit")

    st.sidebar.markdown("### Workbench")
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Speeds_Feeds.py", label="Speeds & Feeds")
    st.sidebar.page_link("pages/2_Threads.py", label="Threads")
    st.sidebar.page_link("pages/3_Calculators.py", label="Math Workbench")
    st.sidebar.page_link("pages/6_G_M_Codes.py", label="G/M Codes & References")
