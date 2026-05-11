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
            "normalize_thread_callout",
            "parse_fractional_number",
            "build_metric_thread_data",
            "build_imperial_thread_data",
            "parse_thread_callout",
            "tap_feed_ipm_from_metric_pitch",
            "calculate_id_thread_values",
            "calculate_od_thread_values",
        },
    )
    normalize = helpers["normalize_thread_callout"]
    helpers["THREAD_SERIES_SUFFIXES"] = ("UNC", "UNF", "UNEF", "UN", "UNS")
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


def test_thread_parser_metric_case_and_tap_feed():
    helpers = load_thread_helpers()

    data = helpers["parse_thread_callout"]("M10x1.5-6H")
    feed = helpers["tap_feed_ipm_from_metric_pitch"](1000, data["pitch_mm"])

    assert data["system"] == "metric"
    assert data["nominal_dia_in"] == pytest.approx(10 / 25.4)
    assert data["pitch_in"] == pytest.approx(1.5 / 25.4)
    assert data["tpi_equiv"] == pytest.approx(25.4 / 1.5)
    assert feed == pytest.approx(1000 * (1.5 / 25.4))


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
