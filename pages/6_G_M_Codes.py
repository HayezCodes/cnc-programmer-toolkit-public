import pandas as pd
import streamlit as st

from data.center_drills import CENTER_DRILL_PRESETS
from data.g_m_codes import G_CODES, M_CODES, SHOP_WARNINGS
from data.general_references import (
    COUNTERSINK_CHAMFER_REFERENCES,
    DECIMAL_FRACTION_ROWS,
    DRILLING_GUIDELINES,
    GM_QUICK_EXAMPLES,
    INSERT_NAMING_BREAKDOWN,
    LOCKNUT_REFERENCE_CATEGORIES,
    LOCKNUT_REFERENCE_NOTE,
    LOCKNUT_WORKFLOW_CHECKS,
    REAMER_ALLOWANCE_REFERENCES,
    REFERENCE_NOTE,
    SPOT_DRILL_ANGLE_REFERENCES,
    SURFACE_FINISH_REFERENCES,
    TAP_DRILL_PERCENT_REFERENCES,
    THREAD_CLASS_REFERENCES,
    TOOLHOLDER_SHORTHAND,
)
from utils.ui_helpers import get_arcwise_logo_path, render_sidebar_nav

st.set_page_config(
    page_title="ArcWise | G & M Codes",
    page_icon=str(get_arcwise_logo_path()) if get_arcwise_logo_path() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1.2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

render_sidebar_nav("G & M Codes")

st.title("G/M Codes & References")
st.caption("General reference only. Code behavior, tooling values, and inspection expectations can vary by machine/control.")

st.warning(
    "MOST IMPORTANT: Verify machine state, active offset, spindle direction, coolant state, tool comp, and tool length before cycle start."
)

tab_codes, tab_holemaking, tab_threads, tab_tooling, tab_finish = st.tabs(
    ["G/M Codes", "Holemaking", "Threads", "Tooling", "Finish & Fits"]
)


with tab_codes:
    search = st.text_input(
        "Search codes or meaning",
        placeholder="Example: G54, coolant, thread, spindle",
    )
    machine_filter = st.selectbox(
        "Machine Type",
        ["All", "Both", "Lathe", "Mill"],
    )

    def filter_df(rows):
        df = pd.DataFrame(rows)

        if search.strip():
            mask = (
                df["code"].str.contains(search, case=False, na=False)
                | df["meaning"].str.contains(search, case=False, na=False)
                | df["note"].str.contains(search, case=False, na=False)
                | df["group"].str.contains(search, case=False, na=False)
            )
            df = df[mask]

        if machine_filter != "All":
            df = df[(df["machine"] == machine_filter) | (df["machine"] == "Both")]

        return df

    st.markdown("### Common G Codes")
    st.dataframe(filter_df(G_CODES), use_container_width=True, hide_index=True)

    st.markdown("### Common M Codes")
    st.dataframe(filter_df(M_CODES), use_container_width=True, hide_index=True)

    st.markdown("### Quick-Use Examples")
    st.dataframe(pd.DataFrame(GM_QUICK_EXAMPLES), use_container_width=True, hide_index=True)

    st.markdown("### Setup Checks")
    for warning in SHOP_WARNINGS:
        st.write(f"- {warning}")


with tab_holemaking:
    st.info(REFERENCE_NOTE)
    st.markdown("### Center Drill Chart")
    center_rows = [
        {
            "Size": size,
            "Style": values["style"],
            "Angle": f"{values['angle']:.0f} deg",
            "Pilot": f"{values['pilot']:.4f}",
            "Body": f"{values['body']:.4f}",
            "Bell": f"{values.get('bell', ''):.4f}" if values.get("bell") else "",
            "Pilot length C": f"{values['pilot_length']:.4f}",
        }
        for size, values in CENTER_DRILL_PRESETS.items()
    ]
    st.dataframe(pd.DataFrame(center_rows), use_container_width=True, hide_index=True)

    with st.expander("Spot drill angle reference", expanded=True):
        st.dataframe(pd.DataFrame(SPOT_DRILL_ANGLE_REFERENCES), use_container_width=True, hide_index=True)

    with st.expander("Countersink / chamfer terminology", expanded=False):
        st.dataframe(pd.DataFrame(COUNTERSINK_CHAMFER_REFERENCES), use_container_width=True, hide_index=True)
        if st.button("Open Spot Drill & Hole Chamfer", use_container_width=True):
            st.switch_page("pages/4_Chamfer_Calculator.py")

    with st.expander("Drill depth and chip evacuation", expanded=False):
        st.dataframe(pd.DataFrame(DRILLING_GUIDELINES), use_container_width=True, hide_index=True)


with tab_threads:
    st.info(REFERENCE_NOTE)
    st.markdown("### Thread Class Quick Reference")
    st.dataframe(pd.DataFrame(THREAD_CLASS_REFERENCES), use_container_width=True, hide_index=True)

    st.markdown("### Tap Drill Percent Starting Points")
    st.dataframe(pd.DataFrame(TAP_DRILL_PERCENT_REFERENCES), use_container_width=True, hide_index=True)

    st.markdown("### Locknuts / Bearing Nuts")
    st.info(LOCKNUT_REFERENCE_NOTE)
    st.dataframe(pd.DataFrame(LOCKNUT_REFERENCE_CATEGORIES), use_container_width=True, hide_index=True)
    with st.expander("Locknut selection checks", expanded=False):
        st.dataframe(pd.DataFrame(LOCKNUT_WORKFLOW_CHECKS), use_container_width=True, hide_index=True)

    if st.button("Open Threads Worksheet", use_container_width=True):
        st.switch_page("pages/2_Threads.py")


with tab_tooling:
    st.info(REFERENCE_NOTE)
    st.markdown("### Insert Naming Breakdown")
    st.dataframe(pd.DataFrame(INSERT_NAMING_BREAKDOWN), use_container_width=True, hide_index=True)

    st.markdown("### Toolholder Shorthand")
    st.dataframe(pd.DataFrame(TOOLHOLDER_SHORTHAND), use_container_width=True, hide_index=True)

    st.markdown("### Decimal / Fraction Conversion")
    st.dataframe(pd.DataFrame(DECIMAL_FRACTION_ROWS), use_container_width=True, hide_index=True)


with tab_finish:
    st.info(REFERENCE_NOTE)
    st.markdown("### Surface Finish Reference")
    st.dataframe(pd.DataFrame(SURFACE_FINISH_REFERENCES), use_container_width=True, hide_index=True)

    st.markdown("### Common Reamer Allowance Starting Points")
    st.dataframe(pd.DataFrame(REAMER_ALLOWANCE_REFERENCES), use_container_width=True, hide_index=True)
