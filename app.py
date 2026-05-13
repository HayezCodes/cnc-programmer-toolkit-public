import streamlit as st
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="CutWise",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1.2rem;
}

.tool-card {
    border: 1px solid rgba(250,250,250,0.14);
    border-radius: 8px;
    padding: 20px 18px 16px 18px;
    background: rgba(255,255,255,0.03);
    min-height: 170px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
}

.tool-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}

.tool-text {
    font-size: 0.93rem;
    opacity: 0.92;
    line-height: 1.35;
}

.home-head {
    border: 1px solid rgba(250,250,250,0.10);
    border-radius: 18px;
    padding: 20px 22px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
}

.section-label {
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 0.75rem;
    margin-bottom: 0.6rem;
    opacity: 0.95;
}

</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Home")

st.markdown("""
<div class="home-head">
    <div style="font-size:0.9rem; opacity:0.8;">PUBLIC CNC PROGRAMMING REFERENCE</div>
    <div style="font-size:2.2rem; font-weight:800; margin-top:0.15rem;">CutWise</div>
    <div style="font-size:0.98rem; opacity:0.85; margin-top:0.35rem;">
        General machining calculators and programming references
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Workbench</div>', unsafe_allow_html=True)

main_col1, main_col2 = st.columns(2)

with main_col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Speeds &amp; Feeds</div>
        <div class="tool-text">Cutting data for lathe, mill, drill, center drill, Woodruff, and tooling references.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Speeds & Feeds", use_container_width=True):
        st.switch_page("pages/1_Speeds_Feeds.py")

with main_col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Threads</div>
        <div class="tool-text">Thread lookup, tap drill and model info, OD estimates, and locknut reference lookup.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Threads", use_container_width=True):
        st.switch_page("pages/2_Threads.py")

main_col3, main_col4 = st.columns(2)

with main_col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Math Workbench</div>
        <div class="tool-text">Holemaking, geometry, conversions, keyway, Woodruff, and drill breakthrough math.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Math Workbench", use_container_width=True):
        st.switch_page("pages/3_Calculators.py")

with main_col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">G/M Codes &amp; References</div>
        <div class="tool-text">Common G/M codes plus general machinist references for holemaking, threading, tooling, and finish.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open G/M Codes & References", use_container_width=True):
        st.switch_page("pages/6_G_M_Codes.py")
