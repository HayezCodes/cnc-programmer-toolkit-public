import pandas as pd
import streamlit as st

from data.g_m_codes import G_CODES, M_CODES, SHOP_WARNINGS
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="G & M Codes",
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

st.title("G & M Codes")
st.caption("General reference only. G-code and M-code behavior can vary by machine/control.")

st.warning(
    "MOST IMPORTANT: Verify machine state, active offset, spindle direction, coolant state, tool comp, and tool length before cycle start."
)

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

st.markdown("### Shop Warnings")
for warning in SHOP_WARNINGS:
    st.write(f"- {warning}")
