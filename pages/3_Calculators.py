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


def calc_hole_chamfer_cleanup_depth(
    finished_dia: float,
    existing_hole_dia: float,
    included_angle_deg: float,
) -> float:
    if finished_dia <= existing_hole_dia:
        raise ValueError("Finished chamfer diameter must be larger than existing hole diameter.")

    if included_angle_deg <= 0 or included_angle_deg >= 180:
        raise ValueError("Included angle must be greater than 0 and less than 180 degrees.")

    half_angle_radians = math.radians(included_angle_deg / 2)
    tangent_value = math.tan(half_angle_radians)

    if abs(tangent_value) < 1e-12:
        raise ValueError("Included angle creates an invalid chamfer calculation.")

    return (finished_dia - existing_hole_dia) / (2 * tangent_value)


SPOT_DRILL_PRESET_ANGLES = {
    "60°": 60.0,
    "82°": 82.0,
    "90°": 90.0,
    "100°": 100.0,
    "118°": 118.0,
    "120°": 120.0,
    "140°": 140.0,
}


def format_woodruff_range(minimum: float, maximum: float) -> str:
    return f"{minimum:.4f} - {maximum:.4f}"


def format_woodruff_target(value: float, tolerance: str) -> str:
    return f"{value:.4f} ({tolerance})"


def format_shop_decimal(value: float, places: int = 4) -> str:
    quantizer = Decimal("1").scaleb(-places)
    adjusted_value = value + 1e-12 if value >= 0 else value - 1e-12
    return format(Decimal(str(adjusted_value)).quantize(quantizer, rounding=ROUND_HALF_UP), f".{places}f")


def build_woodruff_display_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Key Number": row["key_number"],
            "Nominal Size": row["nominal_size"],
            "Cutter Diameter": format_woodruff_range(row["cutter_diameter_min"], row["cutter_diameter_max"]),
            "Keyseat Width": format_woodruff_range(row["keyseat_width_min"], row["keyseat_width_max"]),
            "Shaft Depth": format_woodruff_target(row["shaft_depth"], WOODRUFF_TOLERANCES["shaft_depth"]),
            "Key Above Shaft": format_woodruff_target(row["key_above_shaft"], WOODRUFF_TOLERANCES["key_above_shaft"]),
            "Hub Depth": format_woodruff_target(row["hub_depth"], WOODRUFF_TOLERANCES["hub_depth"]),
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

    display_rows = build_woodruff_display_rows(lookup_rows)

    if len(lookup_rows) == 1:
        row = lookup_rows[0]
        c1, c2 = st.columns(2)
        c1.metric("Key Number", row["key_number"])
        c2.metric("Nominal Size", row["nominal_size"])

    st.table(display_rows)
    st.caption(
        "Source: "
        f"{WOODRUFF_KEY_SOURCE}. "
        "Cutter diameter and keyseat width show ANSI min/max ranges. Shaft depth, key above shaft, and hub depth include ANSI tolerances."
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
        st.markdown("### Drilled Hole Chamfer / Final Z")
        st.write(
            "This is for chamfering an existing drilled/pilot hole. It adds the extra axial depth required "
            "to grow the existing hole diameter to the finished chamfer diameter."
        )

        tool_mode = st.selectbox(
            "Tool Mode",
            [
                "Custom Chamfer / Spot Drill",
                "Center Drill Preset",
                "Spot Drill Preset",
            ],
            key="hole_chamfer_tool_mode"
        )

        included_angle_deg = 90.0
        center_drill_pilot_dia = None
        center_drill_body_dia = None
        center_drill_pilot_length = None
        tool_pilot_length_c = None
        mastercam_check_z = 0.0
        spot_drill_tip_dia = 0.0
        spot_drill_tool_dia = 0.0

        if tool_mode == "Custom Chamfer / Spot Drill":
            included_angle_deg = st.number_input(
                "Chamfer Included Angle (deg)",
                min_value=0.1,
                max_value=179.9,
                value=90.0,
                step=1.0,
                format="%.1f",
                key="hole_chamfer_custom_included_angle"
            )
        elif tool_mode == "Center Drill Preset":
            center_drill_preset = st.selectbox(
                "Center Drill Size",
                get_center_drill_options(include_custom=False),
                format_func=center_drill_select_label,
                key="hole_chamfer_center_drill_preset"
            )
            center_drill_data = CENTER_DRILL_PRESETS[center_drill_preset]
            included_angle_deg = center_drill_data["angle"]
            center_drill_pilot_dia = center_drill_data["pilot"]
            center_drill_body_dia = center_drill_data.get("bell", center_drill_data["body"])
            center_drill_pilot_length = center_drill_data["pilot_length"]

            if st.session_state.get("hole_chamfer_center_drill_preset_state") != center_drill_preset:
                st.session_state["hole_chamfer_center_drill_c_value"] = center_drill_pilot_length
                st.session_state["hole_chamfer_center_drill_mastercam_check_z"] = -0.6550 if center_drill_preset == "8" else 0.0000
                st.session_state["hole_chamfer_center_drill_preset_state"] = center_drill_preset

            preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
            preset_col1.metric("Style", center_drill_data["style"])
            preset_col2.metric("Included Angle", f"{included_angle_deg:.1f} deg")
            preset_col3.metric("Pilot Diameter", f"{center_drill_pilot_dia:.4f}")
            preset_col4.metric("Body / Bell Diameter", f"{center_drill_body_dia:.4f}")

            tool_col1, tool_col2 = st.columns(2)
            with tool_col1:
                tool_pilot_length_c = st.number_input(
                    "Tool Pilot Length / Full Depth Offset (C)",
                    min_value=0.0000,
                    value=st.session_state["hole_chamfer_center_drill_c_value"],
                    step=0.0010,
                    format="%.4f",
                    key="hole_chamfer_center_drill_c_value"
                )
            with tool_col2:
                mastercam_check_z = st.number_input(
                    "Mastercam Check Z",
                    value=st.session_state["hole_chamfer_center_drill_mastercam_check_z"],
                    step=0.0010,
                    format="%.4f",
                    key="hole_chamfer_center_drill_mastercam_check_z"
                )

            st.caption(f"Preset chart C default: {center_drill_pilot_length:.4f}")
            st.caption("Existing hole diameter is the hole already in the part. Center drill pilot diameter is tool geometry.")
            st.caption(
                "Final Program Z uses Tool Pilot Length / Full Depth Offset (C). Adjust C if your Mastercam tool model "
                "or actual center drill does not match the preset."
            )
        else:
            spot_drill_angle_source = st.selectbox(
                "Spot Drill Angle Preset",
                list(SPOT_DRILL_PRESET_ANGLES.keys()) + ["Custom Spot Drill Angle"],
                key="hole_chamfer_spot_drill_angle_source"
            )

            tool_col1, tool_col2, tool_col3 = st.columns(3)
            with tool_col1:
                if spot_drill_angle_source == "Custom Spot Drill Angle":
                    included_angle_deg = st.number_input(
                        "Chamfer Included Angle (deg)",
                        min_value=0.1,
                        max_value=179.9,
                        value=90.0,
                        step=1.0,
                        format="%.1f",
                        key="hole_chamfer_spot_drill_custom_angle"
                    )
                else:
                    included_angle_deg = SPOT_DRILL_PRESET_ANGLES[spot_drill_angle_source]
                    st.metric("Included Angle", f"{included_angle_deg:.1f} deg")
            with tool_col2:
                spot_drill_tip_dia = st.number_input(
                    "Spot Drill Tool Tip Diameter",
                    min_value=0.0000,
                    value=0.0000,
                    step=0.0010,
                    format="%.4f",
                    key="hole_chamfer_spot_drill_tip_dia"
                )
            with tool_col3:
                spot_drill_tool_dia = st.number_input(
                    "Spot Drill Tool Diameter (Optional)",
                    min_value=0.0000,
                    value=0.0000,
                    step=0.0010,
                    format="%.4f",
                    key="hole_chamfer_spot_drill_tool_dia"
                )

            st.caption(
                "Spot Drill Tool Tip Diameter is used for auto base depth. Spot Drill Tool Diameter is only for a size warning "
                "against the finished chamfer diameter."
            )

        base_depth_mode_options = ["Manual"] if tool_mode == "Custom Chamfer / Spot Drill" else ["Auto from Selected Tool", "Manual"]
        default_base_depth_mode = "Manual" if tool_mode == "Custom Chamfer / Spot Drill" else "Auto from Selected Tool"
        if st.session_state.get("hole_chamfer_base_depth_mode_tool_mode") != tool_mode:
            st.session_state["hole_chamfer_base_depth_mode"] = default_base_depth_mode
            st.session_state["hole_chamfer_base_depth_mode_tool_mode"] = tool_mode

        if st.session_state.get("hole_chamfer_base_depth_mode") not in base_depth_mode_options:
            st.session_state["hole_chamfer_base_depth_mode"] = default_base_depth_mode

        input_col1, input_col2, input_col3, input_col4 = st.columns(4)
        with input_col1:
            existing_hole_dia = st.number_input(
                "Existing Drilled / Pilot Hole Diameter",
                min_value=0.0001,
                value=0.4612,
                step=0.0010,
                format="%.4f",
                key="hole_chamfer_existing_dia"
            )
        with input_col2:
            finished_chamfer_dia = st.number_input(
                "Finished Chamfer Major Diameter",
                min_value=0.0001,
                value=0.6250,
                step=0.0010,
                format="%.4f",
                key="hole_chamfer_finished_dia"
            )
        with input_col3:
            backoff_clearance_dia = st.number_input(
                "Backoff / Clearance on Diameter",
                min_value=0.0000,
                value=0.0000,
                step=0.0005,
                format="%.4f",
                key="hole_chamfer_backoff_clearance"
            )
        with input_col4:
            if len(base_depth_mode_options) > 1:
                base_depth_mode = st.selectbox(
                    "Base Depth Mode",
                    base_depth_mode_options,
                    key="hole_chamfer_base_depth_mode"
                )
            else:
                base_depth_mode = "Manual"
                st.caption("Base Depth Mode: Manual")

        if base_depth_mode == "Manual":
            base_hole_depth = st.number_input(
                "Base Pilot / Hole Depth from Face",
                min_value=0.0000,
                value=0.5831,
                step=0.0010,
                format="%.4f",
                key="hole_chamfer_base_depth"
            )
        else:
            base_hole_depth = None

        st.caption("Backoff / Clearance subtracts from the finished chamfer diameter to help avoid cutting the chamfer oversized.")

        target_chamfer_dia = finished_chamfer_dia - backoff_clearance_dia

        invalid_hole_chamfer_inputs = False
        auto_base_warning = None
        diameter_at_final_z = None
        diameter_at_mastercam_z = None
        cleanup_depth = None

        if included_angle_deg <= 0 or included_angle_deg >= 180:
            st.error("Included angle must be greater than 0 and less than 180 degrees.")
            invalid_hole_chamfer_inputs = True

        if base_depth_mode == "Manual" and base_hole_depth < 0:
            st.error("Base pilot / hole depth must be zero or positive.")
            invalid_hole_chamfer_inputs = True

        if backoff_clearance_dia < 0:
            st.error("Backoff / Clearance on Diameter must be zero or positive.")
            invalid_hole_chamfer_inputs = True

        minimum_target_dia = existing_hole_dia
        if tool_mode == "Center Drill Preset":
            minimum_target_dia = max(minimum_target_dia, center_drill_pilot_dia)
        elif tool_mode == "Spot Drill Preset":
            minimum_target_dia = max(minimum_target_dia, spot_drill_tip_dia)

        if target_chamfer_dia <= minimum_target_dia:
            st.error("Backoff is too large. Target chamfer diameter must be larger than the existing hole/tool pilot diameter.")
            invalid_hole_chamfer_inputs = True

        if tool_mode == "Center Drill Preset" and tool_pilot_length_c is not None and tool_pilot_length_c < 0:
            st.error("Tool Pilot Length / Full Depth Offset (C) must be zero or positive.")
            invalid_hole_chamfer_inputs = True

        if not invalid_hole_chamfer_inputs:
            half_angle = math.radians(included_angle_deg / 2)
            cleanup_depth = calc_hole_chamfer_cleanup_depth(
                target_chamfer_dia,
                existing_hole_dia,
                included_angle_deg,
            )

            if tool_mode == "Center Drill Preset":
                if base_depth_mode == "Auto from Selected Tool":
                    if existing_hole_dia <= center_drill_pilot_dia:
                        auto_base_warning = (
                            "Existing hole diameter is smaller than or equal to the center drill pilot diameter. "
                            "Auto base depth may not be valid; verify tool fit or use Manual mode."
                        )

                    base_hole_depth = tool_pilot_length_c + (
                        (existing_hole_dia - center_drill_pilot_dia) / (2 * math.tan(half_angle))
                    )

                full_tool_depth = tool_pilot_length_c + (
                    (target_chamfer_dia - center_drill_pilot_dia) / (2 * math.tan(half_angle))
                )
                final_program_z = -full_tool_depth
                diameter_at_final_z = center_drill_pilot_dia + (
                    2 * (abs(final_program_z) - tool_pilot_length_c) * math.tan(half_angle)
                )

                if mastercam_check_z != 0:
                    if abs(mastercam_check_z) <= tool_pilot_length_c:
                        st.warning("Mastercam Check Z is shallower than Tool Pilot Length / Full Depth Offset (C). The tool has not reached the chamfer cone yet.")
                    else:
                        diameter_at_mastercam_z = center_drill_pilot_dia + (
                            2 * (abs(mastercam_check_z) - tool_pilot_length_c) * math.tan(half_angle)
                        )
            elif tool_mode == "Spot Drill Preset":
                if base_depth_mode == "Auto from Selected Tool":
                    if existing_hole_dia <= spot_drill_tip_dia:
                        auto_base_warning = (
                            "Existing hole diameter is smaller than or equal to the spot drill tip diameter. "
                            "Auto base depth may not be valid; verify tool fit or use Manual mode."
                        )

                    base_hole_depth = (existing_hole_dia - spot_drill_tip_dia) / (2 * math.tan(half_angle))
                    final_program_z = -((target_chamfer_dia - spot_drill_tip_dia) / (2 * math.tan(half_angle)))
                else:
                    final_program_z = -(base_hole_depth + cleanup_depth)

                diameter_at_final_z = spot_drill_tip_dia + (
                    2 * abs(final_program_z) * math.tan(half_angle)
                )
            else:
                final_program_z = -(base_hole_depth + cleanup_depth)
                diameter_at_final_z = target_chamfer_dia

        if not invalid_hole_chamfer_inputs:
            if auto_base_warning:
                st.warning(auto_base_warning)

            result_labels = ["Target Chamfer Diameter", "Final Program Z", "Diameter at Final Program Z"]
            result_values = [
                f"{target_chamfer_dia:.4f}",
                f"{final_program_z:.4f}",
                f"{diameter_at_final_z:.4f}",
            ]

            if diameter_at_mastercam_z is not None:
                result_labels.append("Diameter at Mastercam Check Z")
                result_values.append(f"{diameter_at_mastercam_z:.4f}")

            result_cols = st.columns(len(result_labels))
            for col, label, value in zip(result_cols, result_labels, result_values):
                col.metric(label, value)

            detail_col1, detail_col2 = st.columns(2)
            if cleanup_depth is not None:
                detail_col1.metric("Chamfer Cleanup Axial Depth", f"{cleanup_depth:.4f}")

            if base_depth_mode == "Auto from Selected Tool" and base_hole_depth is not None:
                detail_col2.metric("Auto Base Pilot / Hole Depth from Face", f"{base_hole_depth:.4f}")
            elif base_depth_mode == "Manual":
                detail_col2.metric("Base Pilot / Hole Depth", f"{base_hole_depth:.4f}")

            st.caption(
                "Auto base depth is calculated from the selected tool geometry at the existing hole diameter. "
                "Manual mode lets you override this when your setup or Mastercam reference is different."
            )
            st.caption(
                "Final Program Z is calculated from the target chamfer diameter after backoff/clearance is subtracted."
            )

            if center_drill_body_dia is not None and finished_chamfer_dia > center_drill_body_dia:
                st.warning("Finished chamfer diameter exceeds selected center drill body/bell diameter.")

            if center_drill_body_dia is not None and target_chamfer_dia > center_drill_body_dia:
                st.warning("Target chamfer diameter exceeds selected center drill body/bell diameter.")

            if center_drill_pilot_dia is not None and center_drill_pilot_dia > existing_hole_dia:
                st.warning("Center drill pilot diameter is larger than the existing hole. Verify tool fit before programming.")

            if spot_drill_tool_dia and finished_chamfer_dia > spot_drill_tool_dia:
                st.warning("Finished chamfer diameter exceeds selected spot drill tool diameter.")

            if spot_drill_tool_dia and target_chamfer_dia > spot_drill_tool_dia:
                st.warning("Target chamfer diameter exceeds selected spot drill tool diameter.")

    with st.container(border=True):
        st.markdown("### Centered Slot / Keyway - Both Edges")
        st.write(
            "This mode is for running the tool down the center of a slot/keyway so both top edges are chamfered at the same time. "
            "Use Keyway / Shaft Edge Mode for chamfering only one edge from a wall."
        )
        st.caption(
            "For centered slot/keyway chamfers, the tool must first reach both slot edges before it starts creating the requested edge drop."
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
                value=0.0375,
                step=0.0010,
                format="%.4f",
                key="centered_slot_chamfer_size"
            )
            st.caption(
                "Enter the vertical chamfer drop down the slot wall. Do not use the print's overall chamfer width unless it "
                "represents the same vertical edge drop."
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
                value=0.0100,
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
            centered_slot_tool_cutting_length = st.number_input(
                "Tool Cutting / Taper Length",
                min_value=0.0000,
                value=0.0575,
                step=0.0005,
                format="%.4f",
                key="centered_slot_tool_cutting_length"
            )
            centered_slot_tool_shank_diameter = st.number_input(
                "Tool Shank / Max Diameter",
                min_value=0.0000,
                value=0.2500,
                step=0.0010,
                format="%.4f",
                key="centered_slot_tool_shank_dia"
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

        if centered_slot_tool_cutting_length < 0:
            st.error("Tool cutting / taper length must be zero or positive.")
            centered_slot_invalid = True

        if centered_slot_tool_shank_diameter < 0:
            st.error("Tool shank / max diameter must be zero or positive.")
            centered_slot_invalid = True

        if centered_slot_tip_radius >= centered_slot_half_width:
            st.error("Tool tip diameter is too large for this slot width.")
            centered_slot_invalid = True

        if not centered_slot_invalid:
            centered_slot_half_angle = math.radians(centered_slot_tool_included_angle / 2)
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
                centered_slot_tool_cutting_length - centered_slot_reach_to_edge_depth
            )
            centered_slot_minimum_cutting_length_required = centered_slot_depth_from_top
            centered_slot_shoulder_overtravel = (
                centered_slot_depth_from_top - centered_slot_tool_cutting_length
            )

            primary_col = st.columns(1)[0]
            primary_col.metric("Final Program Z", format_shop_decimal(centered_slot_final_program_z))

            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Half Slot Width", format_shop_decimal(centered_slot_half_width))
            r2.metric("Tip Radius", format_shop_decimal(centered_slot_tip_radius))
            r3.metric("Reach-to-Edge Depth", format_shop_decimal(centered_slot_reach_to_edge_depth))
            r4.metric("Calculated Depth from Top", format_shop_decimal(centered_slot_depth_from_top))

            r5, r6, r7 = st.columns(3)
            r5.metric(
                "Max Clean Chamfer Before Shoulder",
                format_shop_decimal(centered_slot_max_clean_chamfer_before_shoulder)
            )
            r6.metric(
                "Minimum Cutting Length Required",
                format_shop_decimal(centered_slot_minimum_cutting_length_required)
            )
            r7.metric("Shoulder Overtravel", format_shop_decimal(centered_slot_shoulder_overtravel))

            if centered_slot_depth_from_top > centered_slot_tool_cutting_length:
                st.warning("Calculated depth exceeds the tool cutting/taper length. The shank/body may enter the cut.")

            if centered_slot_max_clean_chamfer_before_shoulder < centered_slot_chamfer_size:
                st.warning(
                    "Requested chamfer is larger than this tool can cut cleanly before the shoulder/body enters the slot."
                )

            if (
                centered_slot_tool_shank_diameter > centered_slot_width
                and centered_slot_depth_from_top > centered_slot_tool_cutting_length
            ):
                st.warning(
                    "Tool body/shank is larger than the slot width and the calculated depth goes past the taper length. "
                    "Verify clearance in Mastercam before running."
                )

            st.caption(
                "Example: slot width 0.1885, tool tip diameter 0.1350, 90 deg included tool, vertical edge drop 0.0234375 "
                "gives reach-to-edge depth 0.0268, calculated depth from top 0.0502, and final program Z about -0.0502."
            )

    with st.container(border=True):
        st.markdown("### Keyway / Shaft Edge Mode")
        st.write("Use this when chamfering the straight edge of a keyway or slot on a round shaft.")

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
                "Chamfer Size",
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

        keyway_chamfer_tangent = safe_tangent(keyway_chamfer_angle)
        keyway_tool_half_angle = keyway_tool_included_angle / 2
        keyway_tool_half_tangent = safe_tangent(keyway_tool_half_angle)

        if keyway_width >= shaft_diameter:
            st.error("Keyway width must be smaller than shaft diameter.")
        elif keyway_chamfer_tangent is None:
            st.error("Chamfer angle must be greater than 0 and less than 90 degrees.")
        elif keyway_tool_half_tangent is None:
            st.error("Tool included angle must be greater than 0 and less than 180 degrees.")
        else:
            shaft_radius = shaft_diameter / 2
            half_width = keyway_width / 2
            edge_drop = shaft_radius - math.sqrt(max(0.0, shaft_radius**2 - half_width**2))
            edge_depth = keyway_chamfer_size / keyway_chamfer_tangent
            tip_offset = (keyway_tool_tip_diameter / 2) / keyway_tool_half_tangent
            final_tool_depth_from_edge = edge_depth + tip_offset
            final_programmed_depth = edge_drop + final_tool_depth_from_edge
            tool_offset_from_wall = final_tool_depth_from_edge * keyway_tool_half_tangent
            keyway_tool_angle_matches = abs(keyway_tool_half_angle - keyway_chamfer_angle) <= 0.1

            r1, r2, r3 = st.columns(3)
            r1.metric("Edge Drop from Shaft OD", f"{edge_drop:.4f}")
            r2.metric("Edge Depth from Sharp Edge", f"{edge_depth:.4f}")
            r3.metric("Tool Offset from Wall", f"{tool_offset_from_wall:.4f}")

            r4, r5, r6 = st.columns(3)
            r4.metric("Tip Offset from Sharp Point", f"{tip_offset:.4f}")
            r5.metric("Final Tool Depth from Sharp Edge", f"{final_tool_depth_from_edge:.4f}")
            r6.metric("Final Programmed Depth from Shaft OD Top", f"{final_programmed_depth:.4f}")

            st.write(
                f"Program tool centerline {tool_offset_from_wall:.4f} off wall and "
                f"{final_programmed_depth:.4f} down from shaft OD top."
            )

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
