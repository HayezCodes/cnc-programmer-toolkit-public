import ast
import math
from fractions import Fraction
from pathlib import Path

import pytest

from data.materials import OD_THREADING, TAP_SFM
from data.threads_data import METRIC_THREADS, UN_THREADS
from utils.formulas import (
    drill_feed_ipm,
    ipm_from_ipr,
    ipr_from_ipm,
    rpm_from_sfm,
    sfm_from_rpm,
    tap_feed_ipm_from_tpi,
    tap_feed_mm_min_from_pitch,
)
from utils.holemaking import (
    chamfer_depth_from_diameters,
    chamfer_width_from_depth,
    center_drill_diameter_at_depth,
    center_drill_total_depth_for_target,
    cone_depth_between_diameters,
    target_diameter_from_length_and_angle,
)
from utils.triangle import solve_triangle


ROOT = Path(__file__).resolve().parents[1]


def load_page_functions(page_name: str, function_names: set[str], extra_globals: dict | None = None):
    page_path = ROOT / "pages" / page_name
    source = page_path.read_text(encoding="utf-8")
    module_ast = ast.parse(source, filename=str(page_path))
    selected_nodes = [
        node
        for node in module_ast.body
        if isinstance(node, ast.FunctionDef) and node.name in function_names
    ]
    namespace = {
        "math": math,
        "Fraction": Fraction,
        "re": __import__("re"),
        "TAP_SFM": TAP_SFM,
        "OD_THREADING": OD_THREADING,
        "rpm_from_sfm": rpm_from_sfm,
        "tap_feed_ipm_from_tpi": tap_feed_ipm_from_tpi,
    }
    if extra_globals:
        namespace.update(extra_globals)
    exec(compile(ast.Module(body=selected_nodes, type_ignores=[]), str(page_path), "exec"), namespace)
    return namespace


def load_thread_helpers():
    helpers = load_page_functions(
        "2_Threads.py",
        {
            "apply_cut_mode",
            "has_useful_locknut_value",
            "normalize_thread_callout",
            "parse_fractional_number",
            "build_metric_thread_data",
            "build_imperial_thread_data",
            "parse_thread_callout",
            "extract_thread_fit",
            "format_thread_dimension",
            "locknut_detail_value",
            "build_locknut_thread_detail_block",
            "tap_feed_ipm_from_metric_pitch",
            "calculate_id_thread_values",
            "calculate_od_thread_values",
        },
    )
    normalize = helpers["normalize_thread_callout"]
    helpers["THREAD_SERIES_SUFFIXES"] = ("UNC", "UNF", "UNEF", "UN", "UNS")
    helpers["LOCKNUT_PLACEHOLDER_PATTERNS"] = (
        "catalog lookup required",
        "unknown",
        "tbd",
        "placeholder",
    )
    helpers["UN_THREAD_LOOKUP"] = {normalize(name): values for name, values in UN_THREADS.items()}
    helpers["METRIC_THREAD_LOOKUP"] = {normalize(name): values for name, values in METRIC_THREADS.items()}
    return helpers


def test_rpm_from_sfm_matches_standard_382_constant_reference():
    rpm = rpm_from_sfm(120, 1.0)

    assert rpm == pytest.approx((120 * 12) / math.pi)
    assert rpm == pytest.approx(120 * 3.82, rel=0.001)


def test_sfm_rpm_round_trip_for_positive_diameter():
    rpm = 1500
    diameter = 0.75

    sfm = sfm_from_rpm(rpm, diameter)

    assert rpm_from_sfm(sfm, diameter) == pytest.approx(rpm)


def test_ipm_from_flutes_and_chipload_formula_case():
    rpm = 2000
    flutes = 4
    chipload = 0.002

    ipm = rpm * flutes * chipload

    assert ipm == pytest.approx(16.0)


def test_turning_ipr_stays_ipr_and_converts_to_ipm_intentionally():
    ipr = 0.012
    rpm = 600

    ipm = ipm_from_ipr(ipr, rpm)

    assert ipr == pytest.approx(0.012)
    assert ipm == pytest.approx(7.2)
    assert ipr_from_ipm(ipm, rpm) == pytest.approx(ipr)


def test_drill_and_tap_feed_formulas():
    assert drill_feed_ipm(1000, 0.004) == pytest.approx(4.0)
    assert tap_feed_ipm_from_tpi(650, 13) == pytest.approx(50.0)
    assert tap_feed_ipm_from_tpi(650, 0) == 0
    assert tap_feed_mm_min_from_pitch(1000, 1.25) == pytest.approx(1250.0)


def test_chamfer_target_diameter_assumes_included_angle():
    # 90 degree included angle means a 45 degree side angle, so diameter grows by 2x edge drop.
    assert target_diameter_from_length_and_angle(0.25, 0.01, 90.0) == pytest.approx(0.27)
    assert target_diameter_from_length_and_angle(0.25, 0.01, 90.0, backoff_clearance_dia=0.002) == pytest.approx(0.268)


def test_chamfer_depth_from_pilot_to_target_od():
    assert chamfer_depth_from_diameters(0.25, 0.375, 90.0) == pytest.approx(0.0625)
    assert chamfer_width_from_depth(0.0625, 90.0) == pytest.approx(0.0625)


def test_chamfer_per_side_angle_matches_included_angle():
    per_side_angle = 45.0
    included_angle = per_side_angle * 2

    assert chamfer_depth_from_diameters(0.25, 0.375, included_angle) == pytest.approx(0.0625)


def test_chamfer_rejects_invalid_geometry_inputs():
    with pytest.raises(ValueError):
        chamfer_depth_from_diameters(0.25, 0.25, 90.0)

    with pytest.raises(ValueError):
        chamfer_depth_from_diameters(0.25, 0.375, 180.0)

    with pytest.raises(ValueError):
        chamfer_width_from_depth(-0.001, 90.0)


def test_center_drill_depth_and_diameter_are_inverse_for_90_degree_tool():
    depth = center_drill_total_depth_for_target(
        pilot_dia=0.125,
        target_dia=0.25,
        included_angle_deg=90.0,
        tool_pilot_length_c=0.05,
    )

    assert depth == pytest.approx(0.1125)
    assert center_drill_diameter_at_depth(0.125, 90.0, 0.05, depth) == pytest.approx(0.25)
    assert cone_depth_between_diameters(0.125, 0.25, 90.0) == pytest.approx(0.0625)


def test_center_drill_depth_for_60_degree_included_angle():
    depth = center_drill_total_depth_for_target(
        pilot_dia=0.125,
        target_dia=0.25,
        included_angle_deg=60.0,
        tool_pilot_length_c=0.05,
    )

    assert depth == pytest.approx(0.158253175473)
    assert center_drill_diameter_at_depth(0.125, 60.0, 0.05, depth) == pytest.approx(0.25)


def test_center_drill_rejects_invalid_edge_geometry():
    with pytest.raises(ValueError):
        center_drill_total_depth_for_target(0.125, 0.124, 60.0, 0.0)

    with pytest.raises(ValueError):
        center_drill_total_depth_for_target(0.125, 0.25, 0.0, 0.0)

    with pytest.raises(ValueError):
        center_drill_total_depth_for_target(0.125, 0.25, 60.0, -0.001)


def test_triangle_solver_3_4_5_right_triangle():
    result = solve_triangle(opposite=3, adjacent=4)

    assert result["hypotenuse"] == pytest.approx(5.0)
    assert result["angle"] == pytest.approx(math.degrees(math.atan(3 / 4)))


def test_thread_parser_imperial_fractional_case():
    helpers = load_thread_helpers()

    data = helpers["parse_thread_callout"]("1/2-13 UNC-2B")

    assert data["system"] == "imperial"
    assert data["nominal_dia_in"] == pytest.approx(0.5)
    assert data["pitch_in"] == pytest.approx(1 / 13)
    assert data["pitch_mm"] == pytest.approx((1 / 13) * 25.4)
    assert data["tpi_equiv"] == pytest.approx(13)


def test_speeds_feeds_page_no_longer_contains_quick_tools_shortcuts():
    source = (ROOT / "pages" / "1_Speeds_Feeds.py").read_text(encoding="utf-8")

    assert "Quick Tools" not in source
    assert "Math Workbench" not in source
    assert "G/M Codes & References" not in source


def test_thread_parser_metric_case_and_tap_feed():
    helpers = load_thread_helpers()

    data = helpers["parse_thread_callout"]("M10x1.5-6H")
    feed = helpers["tap_feed_ipm_from_metric_pitch"](1000, data["pitch_mm"])

    assert data["system"] == "metric"
    assert data["nominal_dia_in"] == pytest.approx(10 / 25.4)
    assert data["pitch_in"] == pytest.approx(1.5 / 25.4)
    assert data["tpi_equiv"] == pytest.approx(25.4 / 1.5)
    assert feed == pytest.approx(1000 * (1.5 / 25.4))


def test_thread_fit_extraction_only_returns_explicit_callout_fit():
    helpers = load_thread_helpers()

    assert helpers["extract_thread_fit"]("1/2-13 UNC-2B") == "2B"
    assert helpers["extract_thread_fit"]("M10x1.5-6H") == "6H"
    assert helpers["extract_thread_fit"]("M25x1.5") is None


def test_locknut_thread_detail_block_matches_thread_calculator_style_output():
    helpers = load_thread_helpers()

    data = helpers["parse_thread_callout"]("M25x1.5")
    block = helpers["build_locknut_thread_detail_block"](
        {
            "designation": "KM5",
            "thread": "M25x1.5",
            "matching_lock": "MB5 tab washer where applicable",
            "keyway_spanner_reference": "Requires shaft/sleeve keyway for tab washer.",
        },
        {"label": "KM locknuts"},
        data,
    )

    assert "THREAD: M25x1.5" in block
    assert "TYPE: OD / EXTERNAL LOCKNUT THREAD" in block
    assert "SYSTEM: METRIC" in block
    assert "DESIGNATION / LOCKNUT SIZE: KM5" in block
    assert "NOMINAL / MAJOR DIAMETER: 25.0000 mm (0.9843 in)" in block
    assert "PITCH: 1.5000 mm" in block
    assert f"TPI: {25.4 / 1.5:.4f} equivalent" in block
    assert "CLASS / FIT: NOT AVAILABLE IN SELECTED LOCKNUT CALLOUT." in block
    assert "PITCH DIAMETER ESTIMATE:" in block
    assert "THREAD CALCULATOR OD MODEL: 24.8950 mm (0.9801 in)" in block
    assert "MINOR DIAMETER ESTIMATE:" in block
    assert "BASIC (100% PITCH RULE): 23.5000 mm (0.9252 in)" in block
    assert "75% THREAD DRILL ESTIMATE: 23.8750 mm (0.9400 in)" in block
    assert "MATCHING LOCK / WASHER: MB5 tab washer where applicable" in block
    assert "KEYWAY / SPANNER: Requires shaft/sleeve keyway for tab washer." in block
    assert "VERIFY FINAL DIMENSIONS AGAINST CATALOG / PRINT / GAGE / APPLICABLE STANDARD" in block


def test_id_thread_drill_percent_calculation_uses_pitch_rule():
    helpers = load_thread_helpers()

    values = helpers["calculate_id_thread_values"](
        nominal_dia_in=0.5,
        pitch_in=1 / 13,
        pitch_mm=(1 / 13) * 25.4,
        tpi_equiv=13,
        thread_percent=75,
        material="10 Series Steel",
        system="imperial",
    )

    assert values["recommended_drill_in_basic"] == pytest.approx(0.5 - (1 / 13))
    assert values["recommended_drill_in_percent"] == pytest.approx(0.5 - (0.75 * (1 / 13)))
    assert values["tap_feed"] == pytest.approx(values["tap_rpm"] / 13)


def test_od_thread_model_diameter_and_feed_use_pitch_in_ipr():
    helpers = load_thread_helpers()

    values = helpers["calculate_od_thread_values"](
        nominal_dia_in=0.5,
        pitch_in=1 / 13,
        material="10 Series Steel",
    )

    assert values["model_drop_in"] == pytest.approx(0.07 * (1 / 13))
    assert values["model_dia_in"] == pytest.approx(0.5 - (0.07 * (1 / 13)))
    assert values["estimated_thread_depth_in"] == pytest.approx(0.6495 * (1 / 13))
    assert values["od_ipr"] == pytest.approx(1 / 13)


def test_inch_mm_conversion_reference_cases():
    assert 1.0 * 25.4 == pytest.approx(25.4)
    assert 25.4 / 25.4 == pytest.approx(1.0)
    assert 0.125 * 25.4 == pytest.approx(3.175)
