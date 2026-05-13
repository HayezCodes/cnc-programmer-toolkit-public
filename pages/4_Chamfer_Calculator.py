import streamlit as st

from utils.holemaking import chamfer_depth_from_diameters, chamfer_width_from_depth
from utils.ui_helpers import render_sidebar_nav


st.set_page_config(
    page_title="CutWise | Spot Drill & Hole Chamfer",
    layout="wide",
    initial_sidebar_state="expanded",
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

header[data-testid="stHeader"] {
    height: 0.8rem;
}

.calculator-page-header {
    margin-top: 0.2rem;
    margin-bottom: 0.55rem;
}
</style>
""",
    unsafe_allow_html=True,
)


def format_shop_decimal(value: float, places: int = 4) -> str:
    return f"{value:.{places}f}"


def angle_to_included(angle_mode: str, angle_value: float) -> float:
    if angle_mode == "Per-Side Angle":
        return angle_value * 2
    return angle_value


render_sidebar_nav("Spot Drill & Hole Chamfer")

st.markdown('<div class="calculator-page-header">', unsafe_allow_html=True)
st.title("Spot Drill & Hole Chamfer")
st.caption("Chamfer/countersink depth around holes for spot drills, chamfer mills, and countersinks.")
st.markdown("</div>", unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("Back to Calculators", use_container_width=True):
        st.switch_page("pages/3_Calculators.py")
with nav_col2:
    if st.button("Center Drill Calculator", use_container_width=True):
        st.switch_page("pages/5_Center_Drill_Calculator.py")

with st.container(border=True):
    st.markdown("### Spot Drill / Hole Chamfer / Countersink")
    st.write(
        "Calculates the axial depth needed to grow a pilot or existing hole to a target chamfer/countersink OD."
    )

    input_col1, input_col2, input_col3 = st.columns(3)
    with input_col1:
        pilot_dia = st.number_input(
            "Pilot / Hole Diameter",
            min_value=0.0001,
            value=0.2500,
            step=0.0010,
            format="%.4f",
            key="chamfer_pilot_dia",
        )
        target_od = st.number_input(
            "Target Chamfer OD",
            min_value=0.0001,
            value=0.3750,
            step=0.0010,
            format="%.4f",
            key="chamfer_target_od",
        )
    with input_col2:
        angle_mode = st.radio(
            "Angle Input",
            ["Included Angle", "Per-Side Angle"],
            horizontal=True,
            key="chamfer_angle_mode",
        )
        angle_value = st.number_input(
            "Included Angle (deg)" if angle_mode == "Included Angle" else "Per-Side Angle (deg)",
            min_value=0.1,
            max_value=179.9 if angle_mode == "Included Angle" else 89.95,
            value=90.0 if angle_mode == "Included Angle" else 45.0,
            step=1.0,
            format="%.2f",
            key="chamfer_angle_value",
        )
    with input_col3:
        st.caption("Countersink vs chamfer")
        st.write(
            "A countersink is the conical feature made around a hole. A chamfer is the edge break or angled face."
        )

    included_angle = angle_to_included(angle_mode, angle_value)

    try:
        axial_depth = chamfer_depth_from_diameters(pilot_dia, target_od, included_angle)
        chamfer_width = chamfer_width_from_depth(axial_depth, included_angle)
    except ValueError as exc:
        st.error(str(exc))
    else:
        st.markdown("### Results")
        result_col1, result_col2, result_col3 = st.columns(3)
        result_col1.metric("Axial Depth", format_shop_decimal(axial_depth))
        result_col2.metric("Chamfer Width / Radial Growth", format_shop_decimal(chamfer_width))
        result_col3.metric("Included Angle Used", f"{included_angle:.2f} deg")

        with st.expander("Formula / Assumption Notes", expanded=False):
            st.write("Formula: axial_depth = (target_od - pilot_dia) / (2 * tan(included_angle / 2))")
            st.write("Chamfer width is the radial growth from the pilot/hole diameter to the target OD.")
            st.write("This assumes a simple conical tool or modeled cone with the entered included angle.")
            st.write("Values are general programming geometry; verify against the actual tool and print requirements.")
