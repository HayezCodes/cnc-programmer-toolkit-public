import streamlit as st

from data.center_drills import CENTER_DRILL_PRESETS, center_drill_label, get_center_drill_options
from utils.holemaking import center_drill_diameter_at_depth, center_drill_total_depth_for_target
from utils.ui_helpers import get_arcwise_logo_path, render_sidebar_nav


st.set_page_config(
    page_title="ArcWise | Center Drill Calculator",
    page_icon=str(get_arcwise_logo_path()) if get_arcwise_logo_path() else None,
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


def center_drill_select_label(option: str) -> str:
    if option == "Custom / Pilot Diameter":
        return option
    return center_drill_label(option)


render_sidebar_nav("Center Drill Calculator")

st.markdown('<div class="calculator-page-header">', unsafe_allow_html=True)
st.title("Center Drill Calculator")
st.caption("Finished center or spot diameter depth from pilot diameter and included-angle geometry.")
st.markdown("</div>", unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("Back to Calculators", use_container_width=True):
        st.switch_page("pages/3_Calculators.py")
with nav_col2:
    if st.button("Spot Drill & Hole Chamfer", use_container_width=True):
        st.switch_page("pages/4_Chamfer_Calculator.py")

with st.container(border=True):
    st.markdown("### Center Drill / Spot Diameter")
    st.write(
        "Use this when center drilling the end of a part and you want a target spot diameter on the face."
    )

    preset_options = ["Custom / Pilot Diameter"] + get_center_drill_options(include_custom=False)
    selected_preset = st.selectbox(
        "Center Drill Size or Custom Pilot",
        preset_options,
        format_func=center_drill_select_label,
        key="center_drill_calc_preset",
    )

    if selected_preset == "Custom / Pilot Diameter":
        default_pilot = 0.1250
        default_angle = 60.0
        default_c = 0.0000
        tool_label = "Custom"
        body_dia = None
    else:
        preset = CENTER_DRILL_PRESETS[selected_preset]
        default_pilot = preset["pilot"]
        default_angle = preset["angle"]
        default_c = preset["pilot_length"]
        tool_label = f"Size {selected_preset} ({preset['style']})"
        body_dia = preset.get("bell", preset["body"])

    input_col1, input_col2, input_col3 = st.columns(3)
    with input_col1:
        pilot_dia = st.number_input(
            "Center Drill Pilot Diameter",
            min_value=0.0001,
            value=float(default_pilot),
            step=0.0010,
            format="%.4f",
            key=f"center_drill_calc_pilot_{selected_preset}",
        )
        target_spot_dia = st.number_input(
            "Target Spot Diameter",
            min_value=0.0001,
            value=max(float(default_pilot) + 0.1250, 0.2500),
            step=0.0010,
            format="%.4f",
            key=f"center_drill_calc_target_{selected_preset}",
        )
    with input_col2:
        included_angle = st.number_input(
            "Included Angle Assumption (deg)",
            min_value=0.1,
            max_value=179.9,
            value=float(default_angle),
            step=1.0,
            format="%.2f",
            key=f"center_drill_calc_angle_{selected_preset}",
        )
        pilot_length_c = st.number_input(
            "Pilot Length / C Offset",
            min_value=0.0000,
            value=float(default_c),
            step=0.0010,
            format="%.4f",
            key=f"center_drill_calc_c_{selected_preset}",
        )
    with input_col3:
        st.metric("Tool Reference", tool_label)
        if body_dia is not None:
            st.metric("Body / Bell Diameter", format_shop_decimal(body_dia))

    try:
        required_depth = center_drill_total_depth_for_target(
            pilot_dia,
            target_spot_dia,
            included_angle,
            pilot_length_c,
        )
        diameter_check = center_drill_diameter_at_depth(
            pilot_dia,
            included_angle,
            pilot_length_c,
            required_depth,
        )
    except ValueError as exc:
        st.error(str(exc))
    else:
        st.markdown("### Results")
        result_col1, result_col2, result_col3 = st.columns(3)
        result_col1.metric("Required Depth From Face", format_shop_decimal(required_depth))
        result_col2.metric("Diameter at Depth", format_shop_decimal(diameter_check))
        result_col3.metric("Included Angle Used", f"{included_angle:.2f} deg")

        if body_dia is not None and target_spot_dia > body_dia:
            st.warning("Target spot diameter exceeds the selected center drill body/bell diameter.")

        st.warning(
            "Center drill geometry varies by manufacturer and standard. Verify pilot diameter, C length, "
            "and included angle against the actual tool before cutting."
        )

        with st.expander("Reference Geometry Notes", expanded=False):
            st.write("Formula: depth = C_offset + (target_spot_dia - pilot_dia) / (2 * tan(included_angle / 2))")
            st.write("C offset represents the straight pilot length or the depth offset before the conical section starts.")
            st.write("The target spot diameter is measured at the part face.")
