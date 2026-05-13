import math
from fractions import Fraction
import re
import streamlit as st
import pandas as pd
from data.locknuts import (
    BEARING_LOCKNUT_FAMILY_GUIDE,
    LOCKNUT_DATA,
    LOCKNUT_SERIES,
    LOCKNUT_VERIFICATION_NOTE,
    get_locknut_entry,
    get_locknut_series_options,
    get_locknut_size_options,
)
from data.materials import TAP_SFM, OD_THREADING
from data.general_references import (
    LOCKNUT_REFERENCE_CATEGORIES,
    LOCKNUT_WORKFLOW_CHECKS,
)
from data.threads_data import METRIC_THREADS, UN_THREADS
from utils.formulas import rpm_from_sfm, tap_feed_ipm_from_tpi
from utils.ui_helpers import render_sidebar_nav, render_cutting_mode_sidebar

st.set_page_config(
    page_title="Threads",
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
</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Threads")

render_cutting_mode_sidebar()

st.title("Threads")
st.caption("General thread, tap drill, and modeling reference. Verify final values against the print, gage, and applicable standards.")

THREAD_SERIES_SUFFIXES = ("UNC", "UNF", "UNEF", "UN", "UNS")

LOCKNUT_PLACEHOLDER_PATTERNS = (
    "catalog lookup required",
    "unknown",
    "tbd",
    "placeholder",
)


def has_useful_locknut_value(value) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    if not text:
        return False
    return not any(pattern in text.lower() for pattern in LOCKNUT_PLACEHOLDER_PATTERNS)


def write_locknut_field(label: str, value) -> None:
    if has_useful_locknut_value(value):
        st.write(f"**{label}:** {value}")


def build_visible_locknut_table(rows: list[dict]) -> pd.DataFrame:
    visible_columns = [
        ("designation", "Designation"),
        ("thread", "Thread"),
        ("pitch_tpi", "Pitch / TPI"),
        ("bearing_bore", "Bearing Bore"),
        ("shaft_diameter_reference", "Shaft Reference"),
        ("major_diameter_reference", "Major Diameter"),
        ("matching_lock", "Washer / Lock"),
        ("source_family", "Source Family"),
    ]
    display_rows = []
    for row in rows:
        display_row = {
            heading: row[key]
            for key, heading in visible_columns
            if has_useful_locknut_value(row.get(key))
        }
        display_rows.append(display_row)
    return pd.DataFrame(display_rows)


def apply_cut_mode(value, kind="sfm"):
    return value


def normalize_thread_callout(text: str) -> str:
    cleaned = text.strip().upper().replace("×", "X")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s*X\s*", " X ", cleaned)
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    return cleaned.strip()


UN_THREAD_LOOKUP = {normalize_thread_callout(name): values for name, values in UN_THREADS.items()}
METRIC_THREAD_LOOKUP = {normalize_thread_callout(name): values for name, values in METRIC_THREADS.items()}


def parse_fractional_number(text: str) -> float:
    text = text.strip()

    if " " in text:
        whole, frac = text.split()
        return float(whole) + float(Fraction(frac))

    if "/" in text:
        return float(Fraction(text))

    return float(text)


def build_metric_thread_data(nominal_mm: float, pitch_mm: float):
    if nominal_mm <= 0 or pitch_mm <= 0:
        raise ValueError("Metric thread dimensions must be greater than zero")

    nominal_in = nominal_mm / 25.4
    pitch_in = pitch_mm / 25.4
    tpi_equiv = 25.4 / pitch_mm

    return {
        "system": "metric",
        "display_nominal": nominal_mm,
        "display_pitch": pitch_mm,
        "display_unit": "mm",
        "nominal_dia_in": nominal_in,
        "pitch_in": pitch_in,
        "pitch_mm": pitch_mm,
        "tpi_equiv": tpi_equiv,
    }


def build_imperial_thread_data(nominal_dia_in: float, tpi: float):
    if nominal_dia_in <= 0 or tpi <= 0:
        raise ValueError("Imperial thread dimensions must be greater than zero")

    pitch_in = 1 / tpi
    pitch_mm = pitch_in * 25.4

    return {
        "system": "imperial",
        "display_nominal": nominal_dia_in,
        "display_pitch": tpi,
        "display_unit": "in",
        "nominal_dia_in": nominal_dia_in,
        "pitch_in": pitch_in,
        "pitch_mm": pitch_mm,
        "tpi_equiv": tpi,
    }


def parse_thread_callout(callout: str):
    """
    Supports:
    - Imperial: 1/2-13, 7/8-14, 1 1/4-12, 3.34-12, 1/2-13 UNC-2B
    - Metric: M6x1, M8 x 1.25, M10x1.5, M12 X 1.75, M10x1.5-6H
    """
    raw = normalize_thread_callout(callout)

    if raw in METRIC_THREAD_LOOKUP:
        known_metric = METRIC_THREAD_LOOKUP[raw]
        return build_metric_thread_data(known_metric["major_dia"], known_metric["pitch"])

    if raw in UN_THREAD_LOOKUP:
        known_imperial = UN_THREAD_LOOKUP[raw]
        return build_imperial_thread_data(known_imperial["major_dia"], known_imperial["tpi"])

    metric_match = re.match(r"^M\s*([\d\.]+)\s*X\s*([\d\.]+)(?:\s*[- ]?\s*[A-Z0-9]+)?$", raw)
    if metric_match:
        nominal_mm = float(metric_match.group(1))
        pitch_mm = float(metric_match.group(2))
        return build_metric_thread_data(nominal_mm, pitch_mm)

    imperial_match = re.match(
        r"^([0-9]+(?:\s+[0-9]+/[0-9]+)?|[0-9]+/[0-9]+|[0-9]*\.[0-9]+)\s*-\s*([0-9]+(?:\.[0-9]+)?)(?:\s+.*)?$",
        raw
    )
    if imperial_match:
        nominal_dia = parse_fractional_number(imperial_match.group(1))
        tpi = float(imperial_match.group(2))
        return build_imperial_thread_data(nominal_dia, tpi)

    compact_imperial_match = re.match(
        r"^([0-9]+(?:\.[0-9]+)?(?:/[0-9]+)?)\s*-\s*([0-9]+(?:\.[0-9]+)?)([A-Z].*)$",
        raw
    )
    if compact_imperial_match:
        suffix = compact_imperial_match.group(3)
        if suffix.startswith(THREAD_SERIES_SUFFIXES):
            nominal_dia = parse_fractional_number(compact_imperial_match.group(1))
            tpi = float(compact_imperial_match.group(2))
            return build_imperial_thread_data(nominal_dia, tpi)

    raise ValueError("Invalid thread format")


def tap_feed_ipm_from_metric_pitch(rpm: float, pitch_mm: float) -> float:
    return rpm * (pitch_mm / 25.4)


def extract_thread_fit(callout: str) -> str | None:
    normalized = normalize_thread_callout(callout)
    fit_match = re.search(r"(?:-| )([0-9]+[A-Z]?)$", normalized)
    if not fit_match:
        return None

    fit = fit_match.group(1)
    if re.fullmatch(r"[0-9]+(?:A|B|G|H)", fit):
        return fit
    return None


def format_thread_dimension(value_in: float, system: str) -> str:
    value_mm = value_in * 25.4
    if system == "metric":
        return f"{value_mm:.4f} mm ({value_in:.4f} in)"
    return f"{value_in:.4f} in ({value_mm:.4f} mm)"


def locknut_detail_value(value) -> str:
    if has_useful_locknut_value(value):
        return str(value)
    return "NOT AVAILABLE IN SELECTED LOCKNUT CALLOUT."


def build_locknut_thread_detail_block(
    locknut_entry: dict,
    series_info: dict,
    thread_data: dict,
    thread_percent: int = 75,
) -> str:
    id_values = calculate_id_thread_values(
        nominal_dia_in=thread_data["nominal_dia_in"],
        pitch_in=thread_data["pitch_in"],
        pitch_mm=thread_data["pitch_mm"],
        tpi_equiv=thread_data["tpi_equiv"],
        thread_percent=thread_percent,
        material=next(iter(TAP_SFM)),
        system=thread_data["system"],
    )
    od_values = calculate_od_thread_values(
        nominal_dia_in=thread_data["nominal_dia_in"],
        pitch_in=thread_data["pitch_in"],
        material=next(iter(OD_THREADING)),
    )
    estimated_minor_dia_in = thread_data["nominal_dia_in"] - (2 * od_values["estimated_thread_depth_in"])

    if thread_data["system"] == "metric":
        pitch_display = f"{thread_data['pitch_mm']:.4f} mm"
        tpi_display = f"{thread_data['tpi_equiv']:.4f} equivalent"
    else:
        pitch_display = f"{thread_data['pitch_in']:.6f} in"
        tpi_display = f"{thread_data['tpi_equiv']:.4f}"

    thread_callout = locknut_entry["thread"]
    thread_fit = extract_thread_fit(thread_callout)
    class_fit = thread_fit if thread_fit else "NOT AVAILABLE IN SELECTED LOCKNUT CALLOUT."

    return f"""THREAD: {thread_callout}
TYPE: OD / EXTERNAL LOCKNUT THREAD
SYSTEM: {thread_data["system"].upper()}
DESIGNATION / LOCKNUT SIZE: {locknut_entry["designation"]}
SERIES: {series_info["label"]}

NOMINAL / MAJOR DIAMETER: {format_thread_dimension(thread_data["nominal_dia_in"], thread_data["system"])}
PITCH: {pitch_display}
TPI: {tpi_display}
CLASS / FIT: {class_fit}

PITCH DIAMETER ESTIMATE:
THREAD CALCULATOR OD MODEL: {format_thread_dimension(od_values["model_dia_in"], thread_data["system"])}
MODEL DROP: {format_thread_dimension(od_values["model_drop_in"], thread_data["system"])}

MINOR DIAMETER ESTIMATE:
THREAD DEPTH ESTIMATE: {format_thread_dimension(od_values["estimated_thread_depth_in"], thread_data["system"])}
MINOR FROM NOMINAL - (2 x DEPTH): {format_thread_dimension(estimated_minor_dia_in, thread_data["system"])}

TAP DRILL / MINOR REFERENCE:
BASIC (100% PITCH RULE): {format_thread_dimension(id_values["recommended_drill_in_basic"], thread_data["system"])}
{thread_percent}% THREAD DRILL ESTIMATE: {format_thread_dimension(id_values["recommended_drill_in_percent"], thread_data["system"])}

LOCKNUT DETAILS:
MATCHING LOCK / WASHER: {locknut_detail_value(locknut_entry.get("matching_lock"))}
KEYWAY / SPANNER: {locknut_detail_value(locknut_entry.get("keyway_spanner_reference"))}

VERIFY NOTE:
VERIFY FINAL DIMENSIONS AGAINST CATALOG / PRINT / GAGE / APPLICABLE STANDARD
"""


def calculate_id_thread_values(
    nominal_dia_in: float,
    pitch_in: float,
    pitch_mm: float,
    tpi_equiv: float,
    thread_percent: int,
    material: str,
    system: str,
):
    percent_factor = thread_percent / 100.0
    recommended_drill_in_basic = nominal_dia_in - pitch_in
    recommended_drill_in_percent = nominal_dia_in - (percent_factor * pitch_in)
    recommended_drill_mm_basic = recommended_drill_in_basic * 25.4
    recommended_drill_mm_percent = recommended_drill_in_percent * 25.4

    tap_sfm = apply_cut_mode(TAP_SFM[material], "sfm")
    tap_rpm = rpm_from_sfm(tap_sfm, nominal_dia_in)

    if system == "metric":
        tap_feed = tap_feed_ipm_from_metric_pitch(tap_rpm, pitch_mm)
    else:
        tap_feed = tap_feed_ipm_from_tpi(tap_rpm, tpi_equiv)

    return {
        "recommended_drill_in_basic": recommended_drill_in_basic,
        "recommended_drill_in_percent": recommended_drill_in_percent,
        "recommended_drill_mm_basic": recommended_drill_mm_basic,
        "recommended_drill_mm_percent": recommended_drill_mm_percent,
        "tap_sfm": tap_sfm,
        "tap_rpm": tap_rpm,
        "tap_feed": tap_feed,
    }


def calculate_od_thread_values(nominal_dia_in: float, pitch_in: float, material: str):
    model_drop_in = 0.07 * pitch_in
    model_dia_in = nominal_dia_in - model_drop_in
    model_drop_mm = model_drop_in * 25.4
    model_dia_mm = model_dia_in * 25.4
    nominal_dia_mm = nominal_dia_in * 25.4
    estimated_thread_depth_in = 0.6495 * pitch_in
    estimated_thread_depth_mm = estimated_thread_depth_in * 25.4
    estimated_pass_count = estimated_thread_depth_in / 0.003
    estimated_pass_count_rounded = math.ceil(estimated_pass_count)

    od_sfm = apply_cut_mode(OD_THREADING[material]["sfm"], "sfm")
    od_rpm = rpm_from_sfm(od_sfm, nominal_dia_in)
    od_ipr = apply_cut_mode(pitch_in, "ipr")

    return {
        "model_drop_in": model_drop_in,
        "model_dia_in": model_dia_in,
        "model_drop_mm": model_drop_mm,
        "model_dia_mm": model_dia_mm,
        "nominal_dia_mm": nominal_dia_mm,
        "estimated_thread_depth_in": estimated_thread_depth_in,
        "estimated_thread_depth_mm": estimated_thread_depth_mm,
        "estimated_pass_count": estimated_pass_count,
        "estimated_pass_count_rounded": estimated_pass_count_rounded,
        "od_sfm": od_sfm,
        "od_rpm": od_rpm,
        "od_ipr": od_ipr,
    }



thread_tab, locknut_tab = st.tabs(["Thread Calculator", "Locknut Lookup"])

with thread_tab:
    st.markdown("### Quick Thread Input")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        callout = st.text_input("Thread Callout", value="1/2-13")
        st.caption("Examples: 1/2-13, 1/2-13 UNC-2B, 1 1/4-12, M6x1, M10x1.5-6H")
    
    with c2:
        material = st.selectbox("Material", list(TAP_SFM.keys()))
    
    with c3:
        thread_type = st.selectbox("Type", ["ID", "OD"])
    
    with c4:
        thread_percent = st.selectbox("Percent Thread", [65, 70, 75, 80], index=2)
    
    st.markdown("---")
    
    try:
        thread_data = parse_thread_callout(callout)
    except Exception:
        st.error("Format must be like: 1/2-13, 1/2-13 UNC-2B, 1 1/4-12, M6x1, or M10x1.5-6H")
        st.stop()
    
    system = thread_data["system"]
    nominal_dia_in = thread_data["nominal_dia_in"]
    pitch_in = thread_data["pitch_in"]
    pitch_mm = thread_data["pitch_mm"]
    tpi_equiv = thread_data["tpi_equiv"]
    
    if thread_type == "ID":
        id_values = calculate_id_thread_values(
            nominal_dia_in=nominal_dia_in,
            pitch_in=pitch_in,
            pitch_mm=pitch_mm,
            tpi_equiv=tpi_equiv,
            thread_percent=thread_percent,
            material=material,
            system=system,
        )
    
        if system == "metric":
            st.code(
    f"""THREAD: {callout}
    TYPE: ID
    SYSTEM: METRIC
    MATERIAL: {material}
    
    NOMINAL DIAMETER: {thread_data["display_nominal"]:.4f} mm
    PITCH: {pitch_mm:.4f} mm
    TPI EQUIVALENT: {tpi_equiv:.4f}
    
    RECOMMENDED DRILL:
    BASIC (100% PITCH RULE): {id_values["recommended_drill_mm_basic"]:.4f} mm   ({id_values["recommended_drill_in_basic"]:.4f} in)
    {thread_percent}% THREAD: {id_values["recommended_drill_mm_percent"]:.4f} mm   ({id_values["recommended_drill_in_percent"]:.4f} in)
    
    TAP SFM: {id_values["tap_sfm"]:.0f}
    TAP RPM: {id_values["tap_rpm"]:.0f}
    TAP FEED: {id_values["tap_feed"]:.6f} IPM
    
    NOTES:
    - BASIC DRILL = NOMINAL - PITCH
    - {thread_percent}% THREAD DRILL = NOMINAL - ({thread_percent}% x PITCH)
    - VERIFY FINAL DRILL AGAINST CATALOG / PRINT / GAGE / APPLICABLE STANDARD
    """,
                language="text"
            )
        else:
            st.code(
    f"""THREAD: {callout}
    TYPE: ID
    SYSTEM: IMPERIAL
    MATERIAL: {material}
    
    NOMINAL DIAMETER: {thread_data["display_nominal"]:.4f} in
    TPI: {tpi_equiv:.4f}
    PITCH: {pitch_in:.6f} in   ({pitch_mm:.4f} mm)
    
    RECOMMENDED DRILL:
    BASIC (100% PITCH RULE): {id_values["recommended_drill_in_basic"]:.4f} in   ({id_values["recommended_drill_mm_basic"]:.4f} mm)
    {thread_percent}% THREAD: {id_values["recommended_drill_in_percent"]:.4f} in   ({id_values["recommended_drill_mm_percent"]:.4f} mm)
    
    TAP SFM: {id_values["tap_sfm"]:.0f}
    TAP RPM: {id_values["tap_rpm"]:.0f}
    TAP FEED: {id_values["tap_feed"]:.6f} IPM
    
    NOTES:
    - BASIC DRILL = NOMINAL - PITCH
    - {thread_percent}% THREAD DRILL = NOMINAL - ({thread_percent}% x PITCH)
    - VERIFY FINAL DRILL AGAINST CATALOG / PRINT / GAGE / APPLICABLE STANDARD
    """,
                language="text"
            )
    
    else:
        od_values = calculate_od_thread_values(
            nominal_dia_in=nominal_dia_in,
            pitch_in=pitch_in,
            material=material,
        )
    
        if system == "metric":
            st.code(
    f"""THREAD: {callout}
    TYPE: OD
    SYSTEM: METRIC
    MATERIAL: {material}
    
    NOMINAL DIAMETER: {od_values["nominal_dia_mm"]:.4f} mm   ({nominal_dia_in:.4f} in)
    PITCH: {pitch_mm:.4f} mm
    TPI EQUIVALENT: {tpi_equiv:.4f}
    
    MODEL DIAMETER: {od_values["model_dia_mm"]:.4f} mm   ({od_values["model_dia_in"]:.4f} in)
    MODEL DROP: {od_values["model_drop_mm"]:.4f} mm   ({od_values["model_drop_in"]:.4f} in)
    
    THREAD SFM: {od_values["od_sfm"]:.0f}
    THREAD LEAD / FEED: {od_values["od_ipr"]:.6f} IPR
    APPROX RPM: {od_values["od_rpm"]:.0f}
    
    NOTES:
    - MODEL DIA = NOMINAL - (0.07 x PITCH)
    - OUTPUT MATCHES CURRENT SHOP MEAN-MAJOR APPROXIMATION
    - THREAD FEED = PITCH IN INCHES PER REV
    - VERIFY AGAINST PRINT / GAGE WHEN NEEDED
    """,
                language="text"
            )
    
            st.markdown("### OD Thread Shop Estimate")
            e1, e2, e3 = st.columns(3)
            e1.metric("Pitch", f"{pitch_mm:.4f} mm ({pitch_in:.6f} in)")
            e2.metric(
                "Estimated Thread Depth",
                f"{od_values['estimated_thread_depth_mm']:.4f} mm ({od_values['estimated_thread_depth_in']:.4f} in)"
            )
            e3.metric(
                "Estimated Pass Count (@ .003 radial/pass)",
                f"~{od_values['estimated_pass_count_rounded']}"
            )
    
            st.caption("Shop estimate only. Final pass count still depends on material, insert, machine, and finish requirement.")
        else:
            st.code(
    f"""THREAD: {callout}
    TYPE: OD
    SYSTEM: IMPERIAL
    MATERIAL: {material}
    
    NOMINAL DIAMETER: {nominal_dia_in:.4f} in   ({od_values["nominal_dia_mm"]:.4f} mm)
    TPI: {tpi_equiv:.4f}
    PITCH: {pitch_in:.6f} in   ({pitch_mm:.4f} mm)
    
    MODEL DIAMETER: {od_values["model_dia_in"]:.4f} in   ({od_values["model_dia_mm"]:.4f} mm)
    MODEL DROP: {od_values["model_drop_in"]:.4f} in   ({od_values["model_drop_mm"]:.4f} mm)
    
    THREAD SFM: {od_values["od_sfm"]:.0f}
    THREAD LEAD / FEED: {od_values["od_ipr"]:.6f} IPR
    APPROX RPM: {od_values["od_rpm"]:.0f}
    
    NOTES:
    - MODEL DIA = NOMINAL - (0.07 x PITCH)
    - OUTPUT MATCHES CURRENT SHOP MEAN-MAJOR APPROXIMATION
    - THREAD FEED = 1 / TPI
    - VERIFY AGAINST PRINT / GAGE WHEN NEEDED
    """,
                language="text"
            )
    
            st.markdown("### OD Thread Shop Estimate")
            e1, e2, e3 = st.columns(3)
            e1.metric("Pitch", f"{pitch_in:.6f} in ({pitch_mm:.4f} mm)")
            e2.metric(
                "Estimated Thread Depth",
                f"{od_values['estimated_thread_depth_in']:.4f} in ({od_values['estimated_thread_depth_mm']:.4f} mm)"
            )
            e3.metric(
                "Estimated Pass Count (@ .003 radial/pass)",
                f"~{od_values['estimated_pass_count_rounded']}"
            )
    
            st.caption("Shop estimate only. Final pass count still depends on material, insert, machine, and finish requirement.")

with locknut_tab:
    st.subheader("Locknut Lookup")
    st.caption("Bearing nut and locknut lookup for thread, washer/locking device, and programming checks.")
    st.info(LOCKNUT_VERIFICATION_NOTE)

    lookup_col1, lookup_col2 = st.columns(2)
    with lookup_col1:
        locknut_series = st.selectbox(
            "Locknut Series / Type",
            get_locknut_series_options(),
            format_func=lambda option: LOCKNUT_SERIES[option]["label"],
            key="locknut_lookup_series",
        )
    with lookup_col2:
        locknut_designation = st.selectbox(
            "Size / Designation",
            get_locknut_size_options(locknut_series),
            key="locknut_lookup_designation",
        )

    locknut_entry = get_locknut_entry(locknut_series, locknut_designation)
    series_info = LOCKNUT_SERIES[locknut_series]

    st.markdown("### Selected Locknut")
    info_col1, info_col2, info_col3 = st.columns(3)
    info_col1.metric("Designation", locknut_entry["designation"])
    info_col2.metric("Thread", locknut_entry["thread"])
    info_col3.metric("Pitch / TPI", locknut_entry["pitch_tpi"])

    detail_col1, detail_col2 = st.columns(2)
    with detail_col1:
        write_locknut_field("Series", series_info["label"])
        write_locknut_field("Series Use", series_info["description"])
        write_locknut_field("Matching Lock / Washer", locknut_entry.get("matching_lock"))
        write_locknut_field("Bearing Bore", locknut_entry.get("bearing_bore"))
    with detail_col2:
        write_locknut_field("Major Diameter", locknut_entry.get("major_diameter_reference"))
        write_locknut_field("Shaft Reference", locknut_entry.get("shaft_diameter_reference"))
        write_locknut_field("Keyway / Spanner", locknut_entry.get("keyway_spanner_reference"))

    st.markdown("### Thread Details")
    try:
        locknut_thread_data = parse_thread_callout(locknut_entry["thread"])
        st.code(
            build_locknut_thread_detail_block(locknut_entry, series_info, locknut_thread_data),
            language="text",
        )
        st.caption(
            "General thread references use the same parser and estimate helpers as the Thread Calculator. "
            "Estimated values are starting references only; verify catalog-controlled dimensions before machining."
        )
    except Exception:
        st.code(
            """THREAD DETAILS:
NOT AVAILABLE IN SELECTED LOCKNUT CALLOUT.

VERIFY NOTE:
VERIFY FINAL DIMENSIONS AGAINST CATALOG / PRINT / GAGE / APPLICABLE STANDARD
""",
            language="text",
        )

    st.markdown("### Source / Notes")
    write_locknut_field("Source Family", locknut_entry.get("source_family"))
    write_locknut_field("Source Note", locknut_entry.get("source_note"))

    with st.expander("Series table", expanded=False):
        st.dataframe(build_visible_locknut_table(LOCKNUT_DATA[locknut_series]), use_container_width=True, hide_index=True)

    with st.expander("General locknut selection checks", expanded=False):
        st.dataframe(pd.DataFrame(LOCKNUT_WORKFLOW_CHECKS), use_container_width=True, hide_index=True)
        st.dataframe(pd.DataFrame(LOCKNUT_REFERENCE_CATEGORIES), use_container_width=True, hide_index=True)

    with st.expander("Bearing Locknut Family Guide", expanded=False):
        st.caption("Guide only. This section is not a dimensional lookup; use the selected KM, AN, or N lookup rows or the current manufacturer catalog for size-specific data.")
        st.dataframe(pd.DataFrame(BEARING_LOCKNUT_FAMILY_GUIDE), use_container_width=True, hide_index=True)
