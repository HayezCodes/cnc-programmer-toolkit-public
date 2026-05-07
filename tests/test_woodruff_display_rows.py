import ast
from pathlib import Path

from data.woodruff_keys import (
    WOODRUFF_ANSI_KEY_NOS,
    WOODRUFF_KEY_NOS,
    WOODRUFF_KEY_NUMBERS,
    WOODRUFF_TOLERANCES,
    get_woodruff_key_by_ansi_key_no,
    get_woodruff_key_by_key_no,
    get_woodruff_key_by_number,
)


PAGE_PATH = Path(__file__).resolve().parents[1] / "pages" / "3_Calculators.py"
TARGET_FUNCTIONS = {
    "format_woodruff_range",
    "format_woodruff_target",
    "build_woodruff_primary_display_rows",
    "build_woodruff_hub_display_rows",
}


def load_woodruff_display_helpers():
    source = PAGE_PATH.read_text(encoding="utf-8")
    module_ast = ast.parse(source, filename=str(PAGE_PATH))
    selected_nodes = [
        node
        for node in module_ast.body
        if isinstance(node, ast.FunctionDef) and node.name in TARGET_FUNCTIONS
    ]

    namespace = {"WOODRUFF_TOLERANCES": WOODRUFF_TOLERANCES}
    exec(compile(ast.Module(body=selected_nodes, type_ignores=[]), str(PAGE_PATH), "exec"), namespace)
    return namespace


def test_build_woodruff_primary_display_rows_uses_modeling_column_order_and_mappings():
    helpers = load_woodruff_display_helpers()
    build_woodruff_primary_display_rows = helpers["build_woodruff_primary_display_rows"]

    row = get_woodruff_key_by_number("202")
    assert row is not None

    display_rows = build_woodruff_primary_display_rows([row])
    assert len(display_rows) == 1

    display_row = display_rows[0]
    assert list(display_row.keys()) == [
        "Key No.",
        "ANSI Key No.",
        "Nominal Size",
        "F - Cutter Diameter",
        "A - Keyseat Width",
        "B - Shaft Depth",
        "C - Key Above Shaft",
    ]
    assert display_row["Key No."] == "201"
    assert display_row["ANSI Key No."] == "202"
    assert display_row["Nominal Size"] == "1/16 x 1/4"
    assert display_row["F - Cutter Diameter"] == "0.2500 - 0.2680"
    assert display_row["A - Keyseat Width"] == "0.0615 - 0.0630"
    assert display_row["B - Shaft Depth"] == "0.0728 (+0.005 / -0.000)"
    assert display_row["C - Key Above Shaft"] == "0.0312 (+0.005 / -0.005)"


def test_build_woodruff_hub_display_rows_uses_reference_column_order_and_mappings():
    helpers = load_woodruff_display_helpers()
    build_woodruff_hub_display_rows = helpers["build_woodruff_hub_display_rows"]

    row = get_woodruff_key_by_number("202")
    assert row is not None

    display_rows = build_woodruff_hub_display_rows([row])
    assert len(display_rows) == 1

    display_row = display_rows[0]
    assert list(display_row.keys()) == [
        "Key No.",
        "ANSI Key No.",
        "Nominal Size",
        "D - Hub Width",
        "E - Hub Depth",
    ]
    assert display_row["Key No."] == "201"
    assert display_row["ANSI Key No."] == "202"
    assert display_row["Nominal Size"] == "1/16 x 1/4"
    assert display_row["D - Hub Width"] == "0.0635 (+0.002 / -0.000)"
    assert display_row["E - Hub Depth"] == "0.0372 (+0.005 / -0.000)"


def test_woodruff_lookup_constants_preserve_ansi_backward_compatibility():
    assert WOODRUFF_KEY_NUMBERS == WOODRUFF_ANSI_KEY_NOS
    assert "5" in WOODRUFF_KEY_NOS
    assert "405" in WOODRUFF_ANSI_KEY_NOS


def test_key_no_lookup_returns_matching_ansi_row():
    row = get_woodruff_key_by_key_no("5")
    assert row is not None
    assert row["key_no"] == "5"
    assert row["ansi_key_no"] == "405"
    assert row["key_number"] == "405"
    assert row["nominal_size"] == "1/8 x 5/8"


def test_ansi_lookup_returns_matching_key_no_row():
    row = get_woodruff_key_by_ansi_key_no("405")
    assert row is not None
    assert row["key_no"] == "5"
    assert row["ansi_key_no"] == "405"
    assert row["nominal_size"] == "1/8 x 5/8"


def test_backward_compatible_key_number_lookup_uses_ansi_number():
    row = get_woodruff_key_by_number("405")
    assert row is not None
    assert row["key_no"] == "5"
    assert row["ansi_key_no"] == "405"


def test_validation_examples_from_fastenermart_mapping():
    example_rows = {
        "key_no_7": get_woodruff_key_by_key_no("7"),
        "ansi_809": get_woodruff_key_by_ansi_key_no("809"),
        "key_no_rx": get_woodruff_key_by_key_no("RX"),
        "ansi_2428": get_woodruff_key_by_ansi_key_no("2428"),
    }

    assert example_rows["key_no_7"] is not None
    assert example_rows["key_no_7"]["ansi_key_no"] == "406"
    assert example_rows["key_no_7"]["nominal_size"] == "1/8 x 3/4"

    assert example_rows["ansi_809"] is not None
    assert example_rows["ansi_809"]["key_no"] == "18"
    assert example_rows["ansi_809"]["nominal_size"] == "1/4 x 1-1/8"

    assert example_rows["key_no_rx"] is not None
    assert example_rows["key_no_rx"]["ansi_key_no"] == "822-1"
    assert example_rows["key_no_rx"]["nominal_size"] == "1/4 x 2-3/4"

    assert example_rows["ansi_2428"] is not None
    assert example_rows["ansi_2428"]["key_no"] == "36"
    assert example_rows["ansi_2428"]["nominal_size"] == "3/4 x 3-1/2"
