import streamlit as st
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="Home",
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
    border-radius: 18px;
    padding: 20px 18px 16px 18px;
    background: rgba(255,255,255,0.03);
    min-height: 185px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
}

.tool-icon {
    font-size: 2rem;
    margin-bottom: 0.35rem;
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
    <div style="font-size:0.9rem; opacity:0.8;">PUBLIC CNC PROGRAMMER TOOLKIT</div>
    <div style="font-size:2.2rem; font-weight:800; margin-top:0.15rem;">CNC PROGRAMMING TOOLKIT</div>
    <div style="font-size:0.98rem; opacity:0.85; margin-top:0.35rem;">
        General machining calculators and programming references
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# MAIN
# ---------------------------
st.markdown('<div class="section-label">Main</div>', unsafe_allow_html=True)

main_col1, main_col2 = st.columns(2)

with main_col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">⚙️</div>
        <div class="tool-title">Speeds & Feeds</div>
        <div class="tool-text">Lathe turning, drilling, live tooling, milling, hi-feed reference, and operator notes.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Speeds & Feeds", use_container_width=True):
        st.switch_page("pages/1_Speeds_Feeds.py")

    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🔩</div>
        <div class="tool-title">Threads</div>
        <div class="tool-text">ID and OD thread support with tap feed, drill recommendations, and OD modeling guidance.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Threads", use_container_width=True):
        st.switch_page("pages/2_Threads.py")

# ---------------------------
# TOOLS
# ---------------------------
st.markdown('<div class="section-label">Tools</div>', unsafe_allow_html=True)

tool_col1, tool_col2 = st.columns(2)

with tool_col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">📐</div>
        <div class="tool-title">Calculators</div>
        <div class="tool-text">Triangle, keyway, Woodruff, drill breakthrough, and unit conversion calculators.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Calculators", use_container_width=True):
        st.switch_page("pages/3_Calculators.py")

with tool_col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">⌵</div>
        <div class="tool-title">Chamfer Calculator</div>
        <div class="tool-text">Hole chamfer and countersink depth from pilot diameter, target OD, and angle.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Chamfer Calculator", use_container_width=True):
        st.switch_page("pages/4_Chamfer_Calculator.py")

tool_col3, tool_col4 = st.columns(2)

with tool_col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">◎</div>
        <div class="tool-title">Center Drill Calculator</div>
        <div class="tool-text">Finished center or spot diameter depth with size presets or custom pilot input.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Center Drill Calculator", use_container_width=True):
        st.switch_page("pages/5_Center_Drill_Calculator.py")

with tool_col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🧾</div>
        <div class="tool-title">G &amp; M Codes</div>
        <div class="tool-text">Searchable reference for common G codes, M codes, tool comp, coolant, spindle, offsets, and shop warnings.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("G & M Codes", use_container_width=True):
        st.switch_page("pages/6_G_M_Codes.py")
