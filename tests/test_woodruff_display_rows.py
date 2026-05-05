import ast
from pathlib import Path

from data.woodruff_keys import WOODRUFF_TOLERANCES, get_woodruff_key_by_number


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
        "Nominal Size Key",
        "A - Shaft Width",
        "B - Shaft Depth",
        "F - Cutter Dia",
        "C - Key Above Shaft",
    ]
    assert display_row["A - Shaft Width"] == "0.0615 - 0.0630"
    assert display_row["B - Shaft Depth"] == "0.0728 (+0.005 / -0.000)"
    assert display_row["F - Cutter Dia"] == "0.2500 - 0.2680"
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
        "Nominal Size Key",
        "D - Hub Width",
        "E - Hub Depth",
    ]
    assert display_row["D - Hub Width"] == "0.0635 (+0.002 / -0.000)"
    assert display_row["E - Hub Depth"] == "0.0372 (+0.005 / -0.000)"
