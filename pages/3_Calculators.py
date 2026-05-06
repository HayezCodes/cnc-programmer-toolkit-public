import math
from decimal import Decimal, ROUND_HALF_UP
import streamlit as st
from data.center_drills import CENTER_DRILL_PRESETS, center_drill_label, get_center_drill_options
from data.woodruff_keys import (
    WOODRUFF_KEY_NUMBERS,
    WOODRUFF_KEY_SOURCE,
    WOODRUFF_NOMINAL_SIZES,
    WOODRUFF_TOLERANCES,
    get_woodruff_key_by_number,
    get_woodruff_keys_by_nominal_size,
)
from utils.holemaking import (
    center_drill_diameter_at_depth,
    center_drill_total_depth_for_target,
    derive_center_drill_c_from_full_z,
)
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="Calculators",
    layout="wide",
    initial_sidebar_state="expanded"
)

def center_drill_select_label(option: str) -> str:
    if option == "Custom":
        return "Custom"
    return center_drill_label(option)


def safe_tangent(angle_degrees: float) -> float | None:
    if angle_degrees <= 0 or angle_degrees >= 90:
        return None

    tangent_value = math.tan(math.radians(angle_degrees))
    if abs(tangent_value) < 1e-12:
        return None

    return tangent_value


def format_woodruff_range(minimum: float, maximum: float) -> str:
    return f"{minimum:.4f} - {maximum:.4f}"


def format_woodruff_target(value: float, tolerance: str) -> str:
    return f"{value:.4f} ({tolerance})"


def format_shop_decimal(value: float, places: int = 4) -> str:
    quantizer = Decimal("1").scaleb(-places)
    adjusted_value = value + 1e-12 if value >= 0 else value - 1e-12
    return format(Decimal(str(adjusted_value)).quantize(quantizer, rounding=ROUND_HALF_UP), f".{places}f")


def get_center_drill_full_target_diameter(center_drill_data: dict) -> float:
    return center_drill_data.get("bell", center_drill_data["body"])


def get_center_drill_default_c_details(center_drill_data: dict) -> dict:
    chart_c = center_drill_data["pilot_length"]
    default_c = chart_c
    derived_c = None
    source_label = "Chart C default"
    status_text = "Using chart C default. Verify against Mastercam or edit C if depth does not match."
    warning_text = None

    measured_full_z = center_drill_data.get("mastercam_full_z_depth")
    if center_drill_data.get("full_z_verified") and measured_full_z is not None:
        full_target_dia = get_center_drill_full_target_diameter(center_drill_data)
        measured_full_depth = abs(measured_full_z)
        try:
            derived_c = derive_center_drill_c_from_full_z(
                center_drill_data["pilot"],
                full_target_dia,
                center_drill_data["angle"],
                measured_full_depth,
            )
        except ValueError as exc:
            warning_text = str(exc)
        else:
            if derived_c < 0:
                warning_text = "Derived C from measured full Z is negative. Falling back to chart C default."
            else:
                default_c = derived_c
                source_label = "Shop/Mastercam measured full Z"
                status_text = "Using shop/Mastercam measured full Z depth to derive C."

    return {
        "chart_c": chart_c,
        "default_c": default_c,
        "derived_c": derived_c,
        "source_label": source_label,
        "status_text": status_text,
        "warning_text": warning_text,
    }


def build_woodruff_primary_display_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Key No.": row["key_number"],
            "Nominal Size Key": row["nominal_size"],
            "A - Shaft Width": format_woodruff_range(row["keyseat_width_min"], row["keyseat_width_max"]),
            "B - Shaft Depth": format_woodruff_target(row["shaft_depth"], WOODRUFF_TOLERANCES["shaft_depth"]),
            "F - Cutter Dia": format_woodruff_range(row["cutter_diameter_min"], row["cutter_diameter_max"]),
            "C - Key Above Shaft": format_woodruff_target(row["key_above_shaft"], WOODRUFF_TOLERANCES["key_above_shaft"]),
        }
        for row in rows
    ]


def build_woodruff_hub_display_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Key No.": row["key_number"],
            "Nominal Size Key": row["nominal_size"],
            "D - Hub Width": format_woodruff_target(row["hub_width"], WOODRUFF_TOLERANCES["hub_width"]),
            "E - Hub Depth": format_woodruff_target(row["hub_depth"], WOODRUFF_TOLERANCES["hub_depth"]),
        }
        for row in rows
    ]


st.markdown("""
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

.calc-title-wrap {
    margin-top: 0.2rem;
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Calculators")

st.markdown('<div class="calc-title-wrap">', unsafe_allow_html=True)
st.title("Calculators")
st.caption("Empower MFG - Built for Joshua")
st.markdown("</div>", unsafe_allow_html=True)

tab_triangle, tab_keyway, tab_woodruff, tab_chamfer, tab_breakthrough, tab_convert = st.tabs(
    ["Triangle", "Keyway", "Woodruff Key", "Chamfer", "Drill Breakthrough", "IN ↔ MM"]
)

with tab_triangle:
    st.subheader("Triangle Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use the diagram below so you can fill values in by location.
Right angle is at the bottom left.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<svg width="420" height="220" xmlns="http://www.w3.org/2000/svg">
  <line x1="60" y1="180" x2="60" y2="40" stroke="white" stroke-width="3"/>
  <line x1="60" y1="180" x2="320" y2="180" stroke="white" stroke-width="3"/>
  <line x1="60" y1="40" x2="320" y2="180" stroke="white" stroke-width="3"/>
  <rect x="60" y="165" width="15" height="15" fill="none" stroke="white" stroke-width="2"/>
  <text x="8" y="115" fill="white" font-size="16">Vertical</text>
  <text x="160" y="205" fill="white" font-size="16">Base</text>
  <text x="180" y="95" fill="white" font-size="16">Hypotenuse</text>
  <text x="326" y="175" fill="white" font-size="16">Angle</text>
</svg>
""",
        unsafe_allow_html=True,
    )

    tri_mode = st.selectbox(
        "Solve Using",
        [
            "Vertical + Base",
            "Vertical + Hypotenuse",
            "Base + Hypotenuse",
            "Base + Angle",
            "Vertical + Angle",
            "Hypotenuse + Angle",
        ],
        key="triangle_mode"
    )

    formula_map = {
        "Vertical + Base": "Hyp = √(V² + B²) | Angle = atan(V/B)",
        "Vertical + Hypotenuse": "Base = √(H² - V²) | Angle = asin(V/H)",
        "Base + Hypotenuse": "Vertical = √(H² - B²) | Angle = acos(B/H)",
        "Base + Angle": "V = tan(A)*B | H = B / cos(A)",
        "Vertical + Angle": "B = V / tan(A) | H = V / sin(A)",
        "Hypotenuse + Angle": "B = H*cos(A) | V = H*sin(A)",
    }

    st.markdown(
        f"""
<div style="font-size:0.78rem; opacity:0.75; margin-top:-6px;">
{formula_map[tri_mode]}
</div>
""",
        unsafe_allow_html=True,
    )

    if tri_mode == "Vertical + Base":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_1")
        with col2:
            base = st.number_input("Base", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_1")

        hyp = math.sqrt(vertical**2 + base**2)
        angle = math.degrees(math.atan(vertical / base))

    elif tri_mode == "Vertical + Hypotenuse":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_2")
        with col2:
            hyp = st.number_input("Hypotenuse", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_2")

        if hyp <= vertical:
            st.error("Hypotenuse must be greater than vertical side.")
            st.stop()

        base = math.sqrt(hyp**2 - vertical**2)
        angle = math.degrees(math.asin(vertical / hyp))

    elif tri_mode == "Base + Hypotenuse":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_3")
        with col2:
            hyp = st.number_input("Hypotenuse ", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_3")

        if hyp <= base:
            st.error("Hypotenuse must be greater than base side.")
            st.stop()

        vertical = math.sqrt(hyp**2 - base**2)
        angle = math.degrees(math.acos(base / hyp))

    elif tri_mode == "Base + Angle":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base Side", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_4")
        with col2:
            angle = st.number_input("Angle (deg)", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_4")

        vertical = math.tan(math.radians(angle)) * base
        hyp = base / math.cos(math.radians(angle))

    elif tri_mode == "Vertical + Angle":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical Side  ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_5")
        with col2:
            angle = st.number_input("Angle (deg) ", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_5")

        base = vertical / math.tan(math.radians(angle))
        hyp = vertical / math.sin(math.radians(angle))

    else:
        col1, col2 = st.columns(2)
        with col1:
            hyp = st.number_input("Hypotenuse  ", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_6")
        with col2:
            angle = st.number_input("Angle (deg)  ", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_6")

        base = hyp * math.cos(math.radians(angle))
        vertical = hyp * math.sin(math.radians(angle))

    other_angle = 90 - angle

    c1, c2, c3 = st.columns(3)
    c1.metric("Vertical", f"{vertical:.4f}")
    c2.metric("Base", f"{base:.4f}")
    c3.metric("Hypotenuse", f"{hyp:.4f}")

    c4, c5 = st.columns(2)
    c4.metric("Angle", f"{angle:.4f}")
    c5.metric("Other Angle", f"{other_angle:.4f}")

with tab_keyway:
    st.subheader("Keyway Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Built around the print styles you actually use. Main output is the X value (dia) for programming.
</div>
""",
        unsafe_allow_html=True,
    )

    key_mode = st.selectbox(
        "Callout Style",
        [
            "Bottom of Keyway to Bottom of Shaft",
            "Depth from OD",
            "Width Chord + Depth Below Chord"
        ],
        key="key_mode_v8"
    )

    if key_mode == "Bottom of Keyway to Bottom of Shaft":
        st.markdown(
            """
<svg width="640" height="330" xmlns="http://www.w3.org/2000/svg">
  <circle cx="290" cy="175" r="110" stroke="white" stroke-width="4" fill="none"/>
  <line x1="245" y1="84" x2="245" y2="112" stroke="white" stroke-width="4"/>
  <line x1="335" y1="84" x2="335" y2="112" stroke="white" stroke-width="4"/>
  <line x1="245" y1="112" x2="335" y2="112" stroke="white" stroke-width="4"/>

  <line x1="130" y1="285" x2="290" y2="285" stroke="#999999" stroke-width="4"/>
  <line x1="130" y1="112" x2="245" y2="112" stroke="#999999" stroke-width="4"/>
  <line x1="110" y1="112" x2="110" y2="285" stroke="#999999" stroke-width="4"/>
  <polygon points="110,112 100,126 120,126" fill="#999999"/>
  <polygon points="110,285 100,271 120,271" fill="#999999"/>

  <line x1="480" y1="255" x2="405" y2="215" stroke="#999999" stroke-width="4"/>
  <line x1="480" y1="255" x2="535" y2="255" stroke="#999999" stroke-width="4"/>

  <line x1="290" y1="50" x2="290" y2="300" stroke="#cccccc" stroke-width="2"/>
  <line x1="175" y1="175" x2="405" y2="175" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            shaft_dia = st.number_input("Shaft Diameter", min_value=0.0001, value=1.2500, step=0.1250, format="%.4f", key="kw_bot_dia")
        with col2:
            bottom_to_bottom = st.number_input("Bottom of Keyway to Bottom of Shaft", min_value=0.0001, value=1.1250, step=0.0100, format="%.4f", key="kw_bot_val")

        radius = shaft_dia / 2
        depth_from_od = shaft_dia - bottom_to_bottom
        centerline_to_floor = bottom_to_bottom - radius
        x_value_dia = 2 * centerline_to_floor

        st.markdown("### Results")
        r1, r2 = st.columns(2)
        r1.metric("Depth from OD", f"{depth_from_od:.4f}")
        r2.metric("X Value (Dia)", f"{x_value_dia:.4f}")

    elif key_mode == "Depth from OD":
        st.markdown(
            """
<svg width="640" height="330" xmlns="http://www.w3.org/2000/svg">
  <circle cx="290" cy="175" r="110" stroke="white" stroke-width="4" fill="none"/>
  <line x1="245" y1="84" x2="245" y2="112" stroke="white" stroke-width="4"/>
  <line x1="335" y1="84" x2="335" y2="112" stroke="white" stroke-width="4"/>
  <line x1="245" y1="112" x2="335" y2="112" stroke="white" stroke-width="4"/>

  <line x1="405" y1="75" x2="515" y2="75" stroke="#999999" stroke-width="4"/>
  <line x1="405" y1="112" x2="515" y2="112" stroke="#999999" stroke-width="4"/>
  <line x1="495" y1="75" x2="495" y2="112" stroke="#999999" stroke-width="4"/>
  <polygon points="495,75 484,88 506,88" fill="#999999"/>
  <polygon points="495,112 484,99 506,99" fill="#999999"/>

  <line x1="480" y1="255" x2="405" y2="215" stroke="#999999" stroke-width="4"/>
  <line x1="480" y1="255" x2="535" y2="255" stroke="#999999" stroke-width="4"/>

  <line x1="290" y1="50" x2="290" y2="300" stroke="#cccccc" stroke-width="2"/>
  <line x1="175" y1="175" x2="405" y2="175" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            shaft_dia = st.number_input("Shaft Diameter ", min_value=0.0001, value=1.2500, step=0.1250, format="%.4f", key="kw_top_dia")
        with col2:
            depth_from_od = st.number_input("Depth from OD", min_value=0.0001, value=0.1250, step=0.0100, format="%.4f", key="kw_top_depth")

        radius = shaft_dia / 2
        centerline_to_floor = radius - depth_from_od
        bottom_to_bottom = shaft_dia - depth_from_od
        x_value_dia = 2 * centerline_to_floor

        st.markdown("### Results")
        r1, r2 = st.columns(2)
        r1.metric("X Value (Dia)", f"{x_value_dia:.4f}")
        r2.metric("Bottom of Keyway to Bottom of Shaft", f"{bottom_to_bottom:.4f}")

    else:
        st.markdown(
            """
<svg width="700" height="360" xmlns="http://www.w3.org/2000/svg">
  <circle cx="320" cy="190" r="115" stroke="white" stroke-width="4" fill="none"/>

  <line x1="225" y1="120" x2="415" y2="120" stroke="white" stroke-width="4"/>

  <line x1="225" y1="103" x2="225" y2="137" stroke="#999999" stroke-width="4"/>
  <line x1="415" y1="103" x2="415" y2="137" stroke="#999999" stroke-width="4"/>
  <line x1="225" y1="103" x2="415" y2="103" stroke="#999999" stroke-width="4"/>
  <polygon points="225,103 240,95 240,111" fill="#999999"/>
  <polygon points="415,103 400,95 400,111" fill="#999999"/>

  <line x1="450" y1="120" x2="565" y2="120" stroke="#999999" stroke-width="4"/>
  <line x1="450" y1="160" x2="565" y2="160" stroke="#999999" stroke-width="4"/>
  <line x1="545" y1="120" x2="545" y2="160" stroke="#999999" stroke-width="4"/>
  <polygon points="545,120 535,133 555,133" fill="#999999"/>
  <polygon points="545,160 535,147 555,147" fill="#999999"/>

  <line x1="530" y1="280" x2="450" y2="235" stroke="#999999" stroke-width="4"/>
  <line x1="530" y1="280" x2="590" y2="280" stroke="#999999" stroke-width="4"/>

  <line x1="320" y1="55" x2="320" y2="325" stroke="#cccccc" stroke-width="2"/>
  <line x1="200" y1="190" x2="440" y2="190" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            depth_below_chord = st.number_input("Depth Below Chord", min_value=0.0000, value=0.0000, step=0.0100, format="%.4f", key="kw_chord_depth")
        with col2:
            keyway_width = st.number_input("Keyway Width (Chord)", min_value=0.0001, value=0.3750, step=0.0625, format="%.4f", key="kw_chord_width")
        with col3:
            shaft_dia = st.number_input("Shaft Diameter  ", min_value=0.0001, value=0.8750, step=0.1250, format="%.4f", key="kw_chord_dia")

        radius = shaft_dia / 2
        if keyway_width >= shaft_dia:
            st.error("Keyway width must be smaller than shaft diameter.")
            st.stop()

        chord_x_dia = 2 * math.sqrt(max(0.0, radius**2 - (keyway_width / 2) ** 2))
        final_x_dia = chord_x_dia - (2 * depth_below_chord)
        centerline_to_floor = final_x_dia / 2
        depth_from_od = radius - centerline_to_floor
        bottom_to_bottom = radius + centerline_to_floor

        st.markdown("### Results")
        r1, r2, r3 = st.columns(3)
        r1.metric("Depth from OD", f"{depth_from_od:.4f}")
        r2.metric("Final X Value (Dia)", f"{final_x_dia:.4f}")
        r3.metric("Bottom of Keyway to Bottom of Shaft", f"{bottom_to_bottom:.4f}")

    st.markdown("### Notes")
    st.write("X Value (Dia) is the diameter value from spindle centerline to the keyway floor for programming use.")
    st.write("Width Chord + Depth Below Chord matches the workflow where you model the width as a chord, then step deeper from that line.")

with tab_woodruff:
    st.subheader("Woodruff Key Lookup")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Look up ANSI Woodruff key sizes by key number or by nominal size. Good for checking cutter diameter and keyseat depth before you start programming.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### Chart Letter Guide")
    guide_col1, guide_col2 = st.columns(2)
    with guide_col1:
        st.markdown(
            """
**Primary modeling/programming**

A = shaft keyseat width

B = shaft keyseat depth

F = Woodruff cutter diameter
"""
        )
    with guide_col2:
        st.markdown(
            """
**Reference**

C = key above shaft

D = hub keyseat width

E = hub keyseat depth
"""
        )
    st.caption("Letters match ANSI B17.2 Table 10.")

    lookup_mode = st.radio(
        "Lookup By",
        ["Key Number", "Nominal Size"],
        horizontal=True,
        key="woodruff_lookup_mode"
    )

    if lookup_mode == "Key Number":
        selected_key_number = st.selectbox("Key Number", WOODRUFF_KEY_NUMBERS, key="woodruff_key_number")
        lookup_rows = [get_woodruff_key_by_number(selected_key_number)]
        lookup_rows = [row for row in lookup_rows if row is not None]
    else:
        selected_nominal_size = st.selectbox("Nominal Size", WOODRUFF_NOMINAL_SIZES, key="woodruff_nominal_size")
        lookup_rows = get_woodruff_keys_by_nominal_size(selected_nominal_size)

    primary_display_rows = build_woodruff_primary_display_rows(lookup_rows)
    hub_display_rows = build_woodruff_hub_display_rows(lookup_rows)

    if len(lookup_rows) == 1:
        row = lookup_rows[0]
        c1, c2 = st.columns(2)
        c1.metric("Key Number", row["key_number"])
        c2.metric("Nominal Size", row["nominal_size"])

    st.markdown("### Primary Modeling / Programming Values")
    st.table(primary_display_rows)
    with st.expander("Hub Keyseat Reference D/E", expanded=False):
        st.table(hub_display_rows)
    st.caption(
        "Source: "
        f"{WOODRUFF_KEY_SOURCE}. "
        "A and F show ANSI min/max ranges. B, C, D, and E include ANSI tolerances."
    )

with tab_chamfer:
    st.subheader("Chamfer Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use this for quick edge-break math and for programming chamfer tool depth. Handy for keyway edge breaks and general chamfers.
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("### Center Drill / Finished Center Z")
        st.write(
            "Use this when center drilling the end of a shaft/part and you want a specific finished center diameter on the face."
        )

        center_drill_preset = st.selectbox(
            "Center Drill Size",
            get_center_drill_options(include_custom=False),
            format_func=center_drill_select_label,
            key="center_drill_finished_center_preset"
        )
        center_drill_data = CENTER_DRILL_PRESETS[center_drill_preset]
        center_drill_defaults = get_center_drill_default_c_details(center_drill_data)
        center_drill_pilot_dia = center_drill_data["pilot"]
        center_drill_body_dia = get_center_drill_full_target_diameter(center_drill_data)
        included_angle_deg = center_drill_data["angle"]
        center_drill_selected_size_key = "center_drill_finished_center_selected_size"
        center_drill_c_widget_key = "center_drill_finished_center_c_input"
        derived_default_c = float(center_drill_defaults["default_c"])

        if st.session_state.get(center_drill_selected_size_key) != center_drill_preset:
            st.session_state[center_drill_selected_size_key] = center_drill_preset
            st.session_state[center_drill_c_widget_key] = derived_default_c
        elif center_drill_c_widget_key not in st.session_state:
            st.session_state[center_drill_c_widget_key] = derived_default_c

        tool_info_col1, tool_info_col2, tool_info_col3, tool_info_col4 = st.columns(4)
        tool_info_col1.metric("Style", center_drill_data["style"])
        tool_info_col2.metric("Pilot Diameter", format_shop_decimal(center_drill_pilot_dia))
        tool_info_col3.metric("Included Angle", f"{included_angle_deg:.1f} deg")
        tool_info_col4.metric("Body / Bell Diameter", format_shop_decimal(center_drill_body_dia))

        input_col1, input_col2, input_col3 = st.columns(3)
        with input_col1:
            desired_finished_center_diameter = st.number_input(
                "Desired Finished Center Diameter",
                min_value=0.0001,
                value=0.6250,
                step=0.0010,
                format="%.4f",
                key="center_drill_finished_center_diameter"
            )
            backoff_clearance_dia = st.number_input(
                "Backoff / Clearance on Diameter",
                min_value=0.0000,
                value=0.0000,
                step=0.0005,
                format="%.4f",
                key="center_drill_finished_center_backoff"
            )
        with input_col2:
            top_reference_z = st.number_input(
                "Top Reference Z",
                value=0.0000,
                step=0.0010,
                format="%.4f",
                key="center_drill_finished_center_top_z"
            )
            tool_pilot_length_c = st.number_input(
                "Tool Pilot Length / Full Depth Offset (C)",
                min_value=0.0000,
                step=0.0010,
                format="%.4f",
                key=center_drill_c_widget_key
            )
        with input_col3:
            st.caption(f"Preset chart C default: {format_shop_decimal(center_drill_defaults['chart_c'])}")
            if center_drill_defaults["derived_c"] is not None and center_drill_defaults["derived_c"] >= 0:
                st.caption(f"Derived C from measured full Z: {format_shop_decimal(center_drill_defaults['derived_c'])}")
            if center_drill_data.get("calibration_note"):
                st.caption(center_drill_data["calibration_note"])

        target_center_dia = desired_finished_center_diameter - backoff_clearance_dia
        center_drill_invalid = False
        center_drill_warnings: list[str] = []

        if backoff_clearance_dia < 0:
            st.error("Backoff / Clearance on Diameter must be zero or positive.")
            center_drill_invalid = True

        if tool_pilot_length_c < 0:
            st.error("Tool Pilot Length / Full Depth Offset (C) must be zero or positive.")
            center_drill_invalid = True

        if target_center_dia <= center_drill_pilot_dia:
            st.error("Target center diameter must be larger than the center drill pilot diameter.")
            center_drill_invalid = True

        if target_center_dia > center_drill_body_dia:
            center_drill_warnings.append("Target center diameter exceeds selected center drill body/bell diameter.")

        if center_drill_data.get("full_z_verified") and center_drill_data.get("mastercam_full_z_depth") is not None:
            st.info("Using shop/Mastercam-derived C default.")
        else:
            st.warning("Using chart C default. Verify against Mastercam or edit C if depth does not match.")

        if center_drill_defaults["warning_text"]:
            center_drill_warnings.append(center_drill_defaults["warning_text"])

        if not center_drill_invalid:
            program_depth = center_drill_total_depth_for_target(
                center_drill_pilot_dia,
                target_center_dia,
                included_angle_deg,
                tool_pilot_length_c,
            )
            program_z = top_reference_z - program_depth
            diameter_at_program_z = center_drill_diameter_at_depth(
                center_drill_pilot_dia,
                included_angle_deg,
                tool_pilot_length_c,
                abs(program_z - top_reference_z),
            )

            result_col1, result_col2, result_col3 = st.columns(3)
            result_col1.metric("Target Center Diameter", format_shop_decimal(target_center_dia))
            result_col2.metric("Program Z", format_shop_decimal(program_z))
            result_col3.metric("Diameter at Program Z", format_shop_decimal(diameter_at_program_z))

            with st.expander("Calculation Details", expanded=False):
                st.write(f"Tool C Used: {format_shop_decimal(tool_pilot_length_c)}")
                st.write(f"C Source: {center_drill_defaults['source_label']}")
                st.write(f"Pilot Diameter: {format_shop_decimal(center_drill_pilot_dia)}")
                st.write(f"Included Angle: {included_angle_deg:.1f} deg")
                st.write(f"Body / Bell Diameter: {format_shop_decimal(center_drill_body_dia)}")

        for warning_text in center_drill_warnings:
            st.warning(warning_text)

    with st.container(border=True):
        st.markdown("### Keyway / Slot Chamfer Final Z")
        st.write(
            "Use this for either centered slot/keyway chamfering on both edges or a single edge/wall chamfer along a shaft, slot, or keyway."
        )

        keyway_application_type = st.radio(
            "Application Type",
            ["Centered Slot / Keyway - Both Edges", "Single Edge / Wall Chamfer"],
            horizontal=True,
            key="keyway_chamfer_application_type"
        )

        if keyway_application_type == "Centered Slot / Keyway - Both Edges":
            st.caption(
                "Vertical Edge Drop is the chamfer amount down the slot wall. The tool must first reach both slot edges before cutting that drop."
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                centered_slot_width = st.number_input(
                    "Slot / Keyway Width",
                    min_value=0.0001,
                    value=0.1885,
                    step=0.0010,
                    format="%.4f",
                    key="centered_slot_width"
                )
                centered_slot_chamfer_size = st.number_input(
                    "Desired Chamfer Size / Vertical Edge Drop",
                    min_value=0.0001,
                    value=0.0234375,
                    step=0.0010,
                    format="%.4f",
                    key="centered_slot_chamfer_size"
                )
                centered_slot_top_reference_z = st.number_input(
                    "Top Reference Z",
                    value=0.0000,
                    step=0.0010,
                    format="%.4f",
                    key="centered_slot_top_reference_z"
                )
            with col2:
                centered_slot_tool_included_angle = st.number_input(
                    "Tool Included Angle (deg)",
                    min_value=0.1,
                    max_value=179.9,
                    value=90.0,
                    step=1.0,
                    format="%.1f",
                    key="centered_slot_tool_angle"
                )
                centered_slot_tool_tip_diameter = st.number_input(
                    "Tool Tip Diameter",
                    min_value=0.0000,
                    value=0.1350,
                    step=0.0010,
                    format="%.4f",
                    key="centered_slot_tool_tip_dia"
                )
                centered_slot_cleanup_allowance = st.number_input(
                    "Cleanup / Extra Depth",
                    value=0.0000,
                    step=0.0005,
                    format="%.4f",
                    key="centered_slot_cleanup_allowance"
                )
            with col3:
                centered_slot_tool_body_diameter = st.number_input(
                    "Tool Body / Max Diameter",
                    min_value=0.0000,
                    value=0.2500,
                    step=0.0010,
                    format="%.4f",
                    key="centered_slot_tool_body_dia"
                )

            centered_slot_half_width = centered_slot_width / 2
            centered_slot_tip_radius = centered_slot_tool_tip_diameter / 2
            centered_slot_invalid = False

            if centered_slot_width <= 0:
                st.error("Slot width must be greater than 0.")
                centered_slot_invalid = True

            if centered_slot_chamfer_size <= 0:
                st.error("Desired chamfer size must be greater than 0.")
                centered_slot_invalid = True

            if centered_slot_tool_included_angle <= 0 or centered_slot_tool_included_angle >= 180:
                st.error("Tool included angle must be greater than 0 and less than 180.")
                centered_slot_invalid = True

            if centered_slot_tool_tip_diameter < 0:
                st.error("Tool tip diameter must be zero or positive.")
                centered_slot_invalid = True

            if centered_slot_tool_body_diameter < 0:
                st.error("Tool body/max diameter must be zero or positive.")
                centered_slot_invalid = True

            if centered_slot_tip_radius >= centered_slot_half_width:
                st.error("Tool tip diameter is too large for this slot width.")
                centered_slot_invalid = True

            if centered_slot_tool_body_diameter <= centered_slot_tool_tip_diameter:
                st.error("Tool body/max diameter must be larger than the tool tip diameter.")
                centered_slot_invalid = True

            if not centered_slot_invalid:
                centered_slot_half_angle = math.radians(centered_slot_tool_included_angle / 2)
                centered_slot_calculated_taper_length = (
                    ((centered_slot_tool_body_diameter - centered_slot_tool_tip_diameter) / 2)
                    / math.tan(centered_slot_half_angle)
                )
                centered_slot_reach_to_edge_depth = (
                    (centered_slot_half_width - centered_slot_tip_radius) / math.tan(centered_slot_half_angle)
                )
                centered_slot_depth_from_top = (
                    centered_slot_reach_to_edge_depth
                    + centered_slot_chamfer_size
                    + centered_slot_cleanup_allowance
                )
                centered_slot_final_program_z = centered_slot_top_reference_z - centered_slot_depth_from_top
                centered_slot_max_clean_chamfer_before_shoulder = (
                    centered_slot_calculated_taper_length - centered_slot_reach_to_edge_depth
                )
                centered_slot_minimum_cutting_length_required = centered_slot_depth_from_top
                centered_slot_shoulder_overtravel = (
                    centered_slot_depth_from_top - centered_slot_calculated_taper_length
                )

                primary_col1, primary_col2, primary_col3 = st.columns(3)
                primary_col1.metric("Final Program Z", format_shop_decimal(centered_slot_final_program_z))
                primary_col2.metric("Tool Centerline", "Slot Center")
                primary_col3.metric("Target Vertical Edge Drop", format_shop_decimal(centered_slot_chamfer_size))

                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                detail_col1.metric("Half Slot Width", format_shop_decimal(centered_slot_half_width))
                detail_col2.metric("Tip Radius", format_shop_decimal(centered_slot_tip_radius))
                detail_col3.metric("Reach-to-Edge Depth", format_shop_decimal(centered_slot_reach_to_edge_depth))
                detail_col4.metric("Calculated Depth From Top", format_shop_decimal(centered_slot_depth_from_top))

                if centered_slot_depth_from_top > centered_slot_calculated_taper_length:
                    st.warning("Calculated depth exceeds the tool taper length. The body/shoulder may enter the cut.")

                if centered_slot_max_clean_chamfer_before_shoulder < centered_slot_chamfer_size:
                    st.warning(
                        "Requested chamfer is larger than this tool can cut cleanly before the shoulder/body enters the slot."
                    )

                if (
                    centered_slot_tool_body_diameter > centered_slot_width
                    and centered_slot_depth_from_top > centered_slot_calculated_taper_length
                ):
                    st.warning(
                        "Tool body/max diameter is larger than the slot width and calculated depth goes past taper length. Verify clearance before running."
                    )

                with st.expander("Calculation Details", expanded=False):
                    st.write(
                        f"Calculated Taper Length: {format_shop_decimal(centered_slot_calculated_taper_length)}"
                    )
                    st.write(
                        f"Max Clean Chamfer Before Shoulder: {format_shop_decimal(centered_slot_max_clean_chamfer_before_shoulder)}"
                    )
                    st.write(
                        f"Minimum Cutting Length Required: {format_shop_decimal(centered_slot_minimum_cutting_length_required)}"
                    )
                    st.write(f"Shoulder Overtravel: {format_shop_decimal(centered_slot_shoulder_overtravel)}")

        else:
            st.caption("Use this when chamfering one edge/wall of a keyway, slot, or shaft edge.")

            col1, col2, col3 = st.columns(3)
            with col1:
                shaft_diameter = st.number_input(
                    "Shaft Diameter",
                    min_value=0.0001,
                    value=1.0000,
                    step=0.0100,
                    format="%.4f",
                    key="chamfer_keyway_shaft_dia"
                )
                keyway_width = st.number_input(
                    "Keyway Width",
                    min_value=0.0001,
                    value=0.2500,
                    step=0.0010,
                    format="%.4f",
                    key="chamfer_keyway_width"
                )
            with col2:
                keyway_chamfer_size = st.number_input(
                    "Desired Chamfer Size / Edge Drop",
                    min_value=0.0001,
                    value=0.0050,
                    step=0.0010,
                    format="%.4f",
                    key="chamfer_keyway_size"
                )
                keyway_chamfer_angle = st.number_input(
                    "Chamfer Angle (deg)",
                    min_value=0.1,
                    max_value=89.9,
                    value=45.0,
                    step=1.0,
                    format="%.1f",
                    key="chamfer_keyway_angle"
                )
            with col3:
                keyway_tool_included_angle = st.number_input(
                    "Tool Included Angle (deg)",
                    min_value=1.0,
                    max_value=179.9,
                    value=90.0,
                    step=1.0,
                    format="%.1f",
                    key="chamfer_keyway_tool_angle"
                )
                keyway_tool_tip_diameter = st.number_input(
                    "Tool Tip Diameter",
                    min_value=0.0000,
                    value=0.0100,
                    step=0.0010,
                    format="%.4f",
                    key="chamfer_keyway_tool_tip"
                )
                keyway_tool_body_diameter = st.number_input(
                    "Tool Body / Max Diameter",
                    min_value=0.0000,
                    value=0.2500,
                    step=0.0010,
                    format="%.4f",
                    key="chamfer_keyway_tool_body_dia"
                )

            keyway_chamfer_tangent = safe_tangent(keyway_chamfer_angle)
            keyway_tool_half_angle = keyway_tool_included_angle / 2
            keyway_tool_half_tangent = safe_tangent(keyway_tool_half_angle)

            if keyway_width >= shaft_diameter:
                st.error("Keyway width must be smaller than shaft diameter.")
            elif keyway_chamfer_tangent is None:
                st.error("Chamfer angle must be greater than 0 and less than 90 degrees.")
            elif keyway_tool_half_tangent is None:
                st.error("Tool included angle must be greater than 0 and less than 180 degrees.")
            elif keyway_tool_tip_diameter < 0:
                st.error("Tool tip diameter must be zero or positive.")
            elif keyway_tool_body_diameter <= keyway_tool_tip_diameter:
                st.error("Tool body/max diameter must be larger than the tool tip diameter.")
            else:
                shaft_radius = shaft_diameter / 2
                half_width = keyway_width / 2
                edge_drop = shaft_radius - math.sqrt(max(0.0, shaft_radius**2 - half_width**2))
                edge_depth = keyway_chamfer_size / keyway_chamfer_tangent
                tip_offset = (keyway_tool_tip_diameter / 2) / keyway_tool_half_tangent
                keyway_calculated_taper_length = (
                    ((keyway_tool_body_diameter - keyway_tool_tip_diameter) / 2)
                    / math.tan(math.radians(keyway_tool_included_angle / 2))
                )
                final_tool_depth_from_edge = edge_depth + tip_offset
                final_programmed_depth = edge_drop + final_tool_depth_from_edge
                tool_offset_from_wall = final_tool_depth_from_edge * keyway_tool_half_tangent
                keyway_tool_angle_matches = abs(keyway_tool_half_angle - keyway_chamfer_angle) <= 0.1

                result_col1, result_col2, result_col3 = st.columns(3)
                result_col1.metric("Tool Offset From Wall", format_shop_decimal(tool_offset_from_wall))
                result_col2.metric("Final Program Depth / Z", format_shop_decimal(final_programmed_depth))
                result_col3.metric("Edge Drop From Shaft OD", format_shop_decimal(edge_drop))

                with st.expander("Calculation Details", expanded=False):
                    st.write(f"Tip Offset: {format_shop_decimal(tip_offset)}")
                    st.write(f"Calculated Taper Length: {format_shop_decimal(keyway_calculated_taper_length)}")
                    st.write(f"Tool Side Angle Check: {keyway_tool_half_angle:.1f} deg vs chamfer {keyway_chamfer_angle:.1f} deg")
                    st.write(f"Edge Depth from Sharp Edge: {format_shop_decimal(edge_depth)}")
                    st.write(f"Final Tool Depth from Sharp Edge: {format_shop_decimal(final_tool_depth_from_edge)}")

                if keyway_tool_angle_matches:
                    st.info("This tool angle matches the requested chamfer geometry for a clean edge break.")
                else:
                    st.warning(
                        f"Tool side angle is {keyway_tool_half_angle:.1f} deg, but the requested chamfer angle is {keyway_chamfer_angle:.1f} deg. "
                        "This tool will not make that chamfer cleanly."
                    )

with tab_breakthrough:
    st.subheader("Drill Breakthrough Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use this to figure the extra drill travel needed after the point first reaches the far side.
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        drill_diameter = st.number_input("Drill Diameter", min_value=0.0001, value=0.2500, step=0.0010, format="%.4f", key="breakthrough_dia")
    with col2:
        point_angle = st.number_input("Point Angle (deg)", min_value=1.0, max_value=179.0, value=118.0, step=1.0, format="%.1f", key="breakthrough_angle")
    with col3:
        breakthrough_past_center = st.number_input("Breakthrough Past Center", min_value=0.0000, value=0.0200, step=0.0010, format="%.4f", key="breakthrough_past_center")

    point_height_to_center = (drill_diameter / 2) / math.tan(math.radians(point_angle / 2))
    additional_depth_required = point_height_to_center + breakthrough_past_center
    total_drill_depth = additional_depth_required

    st.markdown("### Results")
    r1, r2 = st.columns(2)
    r1.metric("Additional Depth Required", f"{additional_depth_required:.4f}")
    r2.metric("Total Drill Depth", f"{total_drill_depth:.4f}")

    st.write("Total drill depth is referenced from the moment the drill point first contacts the back side of the part.")

with tab_convert:
    st.subheader("IN ↔ MM Converter")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Convert either direction. Enter a value in the side you want to use.
</div>
""",
        unsafe_allow_html=True,
    )

    convert_mode = st.radio("Conversion Direction", ["IN to MM", "MM to IN"], horizontal=True, key="unit_convert_mode")

    if convert_mode == "IN to MM":
        inches = st.number_input("Inches", min_value=0.0000, value=1.0000, step=0.0010, format="%.4f", key="inch_input")
        mm = inches * 25.4

        c1, c2 = st.columns(2)
        c1.metric("Inches", f"{inches:.4f}")
        c2.metric("Millimeters", f"{mm:.4f}")

    else:
        mm = st.number_input("Millimeters", min_value=0.0000, value=25.4000, step=0.0100, format="%.4f", key="mm_input")
        inches = mm / 25.4

        c1, c2 = st.columns(2)
        c1.metric("Millimeters", f"{mm:.4f}")
        c2.metric("Inches", f"{inches:.4f}")

    st.markdown("### Quick Reference")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("1/16 in", f"{0.0625 * 25.4:.4f} mm")
    q2.metric("1/8 in", f"{0.1250 * 25.4:.4f} mm")
    q3.metric("1/4 in", f"{0.2500 * 25.4:.4f} mm")
    q4.metric("1 in", f"{1.0000 * 25.4:.4f} mm")
