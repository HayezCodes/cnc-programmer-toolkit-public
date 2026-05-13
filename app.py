import base64

import streamlit as st
from utils.ui_helpers import get_arcwise_logo_path, render_sidebar_nav

st.set_page_config(
    page_title="ArcWise",
    page_icon=str(get_arcwise_logo_path()) if get_arcwise_logo_path() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 1.35rem;
    padding-bottom: 1.2rem;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(23, 127, 255, 0.18), transparent 34rem),
        linear-gradient(180deg, #060b12 0%, #08111b 48%, #070a0f 100%);
}

.tool-card {
    border: 1px solid rgba(88, 173, 255, 0.18);
    border-radius: 8px;
    padding: 16px 17px 15px;
    background:
        linear-gradient(180deg, rgba(18, 38, 58, 0.82), rgba(7, 14, 23, 0.94));
    min-height: 166px;
    box-shadow: 0 16px 42px rgba(0,0,0,0.26), 0 0 0 1px rgba(255,255,255,0.025) inset;
    transition: border-color 160ms ease, transform 160ms ease, box-shadow 160ms ease;
}

.tool-card:hover {
    border-color: rgba(89, 184, 255, 0.42);
    box-shadow: 0 18px 48px rgba(0,0,0,0.30), 0 0 28px rgba(25, 130, 255, 0.10);
    transform: translateY(-1px);
}

.tool-icon {
    align-items: center;
    background: rgba(58, 157, 255, 0.12);
    border: 1px solid rgba(89, 184, 255, 0.20);
    border-radius: 8px;
    color: #d9f0ff;
    display: inline-flex;
    font-size: 1.45rem;
    height: 42px;
    justify-content: center;
    line-height: 1;
    margin-bottom: 0.75rem;
    width: 42px;
}

.tool-title {
    color: #edf7ff;
    font-size: 1.04rem;
    font-weight: 760;
    margin-bottom: 0.38rem;
}

.tool-text {
    color: #b8c8d9;
    font-size: 0.91rem;
    line-height: 1.38;
}

.home-head {
    border: 1px solid rgba(83, 167, 255, 0.18);
    border-radius: 8px;
    padding: 24px 22px 20px;
    background:
        radial-gradient(circle at center top, rgba(40, 150, 255, 0.18), transparent 16rem),
        linear-gradient(180deg, rgba(12, 28, 45, 0.94), rgba(6, 13, 22, 0.96));
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28), inset 0 -1px 0 rgba(82, 169, 255, 0.12);
    margin-bottom: 0.85rem;
    overflow: hidden;
    position: relative;
    text-align: center;
}

.home-head:after {
    background: linear-gradient(90deg, transparent, rgba(86, 186, 255, 0.55), transparent);
    bottom: 0;
    content: "";
    height: 1px;
    left: 14%;
    position: absolute;
    right: 14%;
}

.hero-logo {
    display: block;
    margin: 0 auto 0.65rem;
    max-width: 250px;
    width: 36%;
}

.hero-logo-fallback {
    color: #edf8ff;
    font-size: 2.65rem;
    font-weight: 820;
    letter-spacing: 0.035em;
    margin-bottom: 0.55rem;
}

.hero-subtitle {
    color: #9fb7d1;
    font-size: 0.82rem;
    font-weight: 720;
    letter-spacing: 0.12em;
    line-height: 1.45;
    text-transform: uppercase;
}

.section-label {
    color: #dceeff;
    font-size: 0.82rem;
    font-weight: 760;
    letter-spacing: 0.12em;
    margin-top: 0.55rem;
    margin-bottom: 0.65rem;
    text-transform: uppercase;
}

div.stButton > button {
    border-color: rgba(83, 167, 255, 0.22);
    border-radius: 8px;
    color: #dceeff;
}

</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Home")

logo_path = get_arcwise_logo_path()
if logo_path:
    logo_markup = (
        f'<img class="hero-logo" src="data:image/png;base64,'
        f'{base64.b64encode(logo_path.read_bytes()).decode("ascii")}" alt="ArcWise logo">'
    )
else:
    logo_markup = '<div class="hero-logo-fallback">ArcWise</div>'

st.markdown(f"""
<div class="home-head">
    {logo_markup}
    <div class="hero-subtitle">GENERAL MACHINING CALCULATORS AND PROGRAMMING REFERENCES</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Workbench</div>', unsafe_allow_html=True)


def render_tool_card(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
    <div class="tool-card">
        <div class="tool-icon">{icon}</div>
        <div class="tool-title">{title}</div>
        <div class="tool-text">{description}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


dashboard_cards = [
    (
        "⚙️",
        "Speeds &amp; Feeds",
        "Cutting data for lathe, mill, drill, center drill, Woodruff, and tooling references.",
        "Open Speeds & Feeds",
        "pages/1_Speeds_Feeds.py",
    ),
    (
        "🔩",
        "Threads",
        "Thread lookup, tap drill and model info, OD estimates, and locknut reference lookup.",
        "Open Threads",
        "pages/2_Threads.py",
    ),
    (
        "📐",
        "Math Workbench",
        "Holemaking, geometry, conversions, keyway, Woodruff, and drill breakthrough math.",
        "Open Math Workbench",
        "pages/3_Calculators.py",
    ),
    (
        "📜",
        "G/M Codes &amp; References",
        "Common G/M codes plus general machinist references for holemaking, threading, tooling, and finish.",
        "Open G/M Codes & References",
        "pages/6_G_M_Codes.py",
    ),
    (
        "◺",
        "Chamfer Calculator",
        "Spot drill, countersink, and hole chamfer depth from included angle and target diameter.",
        "Open Chamfer Calculator",
        "pages/4_Chamfer_Calculator.py",
    ),
    (
        "🎯",
        "Center Drill Calculator",
        "Finished center or spot diameter depth from pilot diameter and included-angle geometry.",
        "Open Center Drill Calculator",
        "pages/5_Center_Drill_Calculator.py",
    ),
]

for row_start in range(0, len(dashboard_cards), 3):
    columns = st.columns(3)
    for column, (icon, title, description, button_label, page) in zip(columns, dashboard_cards[row_start:row_start + 3]):
        with column:
            render_tool_card(icon, title, description)
            if st.button(button_label, use_container_width=True):
                st.switch_page(page)
