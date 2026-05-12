from data import general_references as refs
from data.center_drills import CENTER_DRILL_PRESETS
from data.locknuts import (
    BEARING_LOCKNUT_FAMILY_GUIDE,
    LOCKNUT_DATA,
    LOCKNUT_VERIFICATION_NOTE,
    REQUIRED_LOCKNUT_FIELDS,
    get_locknut_entry,
    get_locknut_series_options,
    get_locknut_size_options,
)


LOCKNUT_VISIBLE_FIELDS = (
    "designation",
    "series",
    "thread",
    "pitch_tpi",
    "matching_lock",
    "bearing_bore",
    "shaft_diameter_reference",
    "major_diameter_reference",
    "source_family",
    "source_note",
    "programming_notes",
)

LOCKNUT_PLACEHOLDER_TEXT = (
    "catalog lookup required",
    "tbd",
    "unknown",
    "placeholder",
    "manufacturer_catalog_required",
    "verification_required",
)


def test_general_reference_tables_have_public_rows():
    tables = [
        refs.SPOT_DRILL_ANGLE_REFERENCES,
        refs.COUNTERSINK_CHAMFER_REFERENCES,
        refs.DRILLING_GUIDELINES,
        refs.THREAD_CLASS_REFERENCES,
        refs.LOCKNUT_REFERENCE_CATEGORIES,
        refs.LOCKNUT_WORKFLOW_CHECKS,
        refs.TAP_DRILL_PERCENT_REFERENCES,
        refs.INSERT_NAMING_BREAKDOWN,
        refs.SURFACE_FINISH_REFERENCES,
        refs.REAMER_ALLOWANCE_REFERENCES,
        refs.TOOLHOLDER_SHORTHAND,
        refs.DECIMAL_FRACTION_ROWS,
        refs.GM_QUICK_EXAMPLES,
    ]

    for table in tables:
        assert table
        for row in table:
            assert all(str(value).strip() for value in row.values())


def test_center_drill_presets_are_chart_style_public_references():
    for preset in CENTER_DRILL_PRESETS.values():
        assert "mastercam_full_z_depth" not in preset
        assert "shop" not in preset.get("calibration_note", "").lower()
        assert preset["pilot"] > 0
        assert preset["body"] > 0
        assert 0 < preset["angle"] < 180


def test_locknut_references_are_marked_catalog_reference_only():
    assert "SKF" in refs.LOCKNUT_REFERENCE_NOTE
    assert "Timken" in refs.LOCKNUT_REFERENCE_NOTE
    assert "Whittet-Higgins" in refs.LOCKNUT_REFERENCE_NOTE
    assert "current catalog before machining" in refs.LOCKNUT_REFERENCE_NOTE
    assert {row["Family"] for row in refs.LOCKNUT_REFERENCE_CATEGORIES} >= {
        "KM locknuts",
        "AN locknuts",
        "N locknuts",
        "Bearing locknuts",
    }


def test_locknut_lookup_data_loads_required_series_and_sizes():
    assert set(get_locknut_series_options()) == {"KM", "AN", "N"}
    assert get_locknut_series_options() == ["KM", "AN", "N"]
    assert "Bearing locknut" not in get_locknut_series_options()
    assert {"KM0", "KM10"}.issubset(set(get_locknut_size_options("KM")))
    assert {"AN 15", "AN 40"}.issubset(set(get_locknut_size_options("AN")))
    assert {"N 07", "N 14"}.issubset(set(get_locknut_size_options("N")))


def test_bearing_locknut_family_guide_is_not_selectable_lookup_data():
    assert BEARING_LOCKNUT_FAMILY_GUIDE
    assert "Bearing locknut" not in LOCKNUT_DATA
    assert {
        "KM / KML metric bearing locknuts",
        "N inch bearing locknuts",
        "AN inch bearing locknuts",
        "HM / HME larger metric bearing locknuts",
        "Integral-locking locknuts",
    }.issubset({row["Family"] for row in BEARING_LOCKNUT_FAMILY_GUIDE})

    for row in BEARING_LOCKNUT_FAMILY_GUIDE:
        assert "not a dimensional lookup" in row["Guide note"]
        assert row["Catalog family to check"]
        assert row["What to verify"]


def test_locknut_size_lookup_returns_required_fields_and_verification_notes():
    km_entry = get_locknut_entry("KM", "KM5")
    an_entry = get_locknut_entry("AN", "AN 20")
    n_entry = get_locknut_entry("N", "N 10")

    assert set(REQUIRED_LOCKNUT_FIELDS).issubset(km_entry)
    assert km_entry["thread"] == "M25x1.5"
    assert km_entry["thread_size"] == "M25"
    assert km_entry["pitch_tpi"] == "1.5 mm"
    assert "SKF" in km_entry["verification_note"]
    assert LOCKNUT_VERIFICATION_NOTE == (
        "Verify final dimensions, thread, washer, and spanner details with SKF, Timken, "
        "Whittet-Higgins, or the locknut manufacturer before machining."
    )
    assert km_entry["verification_required"] is True
    assert km_entry["manufacturer_catalog_required"] is True

    assert an_entry["bearing_bore"] == "100 mm"
    assert an_entry["thread"] == "3.918-12 TPI"
    assert an_entry["matching_lock"] == "W 20"
    assert "Timken" in an_entry["source_family"]

    assert n_entry["bearing_bore"] == "50 mm"
    assert n_entry["thread"] == "1.967-18 TPI"
    assert n_entry["matching_lock"] == "W 10"
    assert "Timken" in n_entry["source_family"]

    for rows in LOCKNUT_DATA.values():
        for row in rows:
            assert set(REQUIRED_LOCKNUT_FIELDS).issubset(row)
            assert row["series"]
            assert row["designation"]
            assert row["thread"]
            assert row["source_family"]
            assert row["source_note"]
            assert row["verification_note"]
            assert row["verification_required"] is True
            assert row["manufacturer_catalog_required"] is True
            assert "final production dimensions" not in row["source_note"].lower()


def test_visible_locknut_fields_do_not_contain_placeholder_text():
    for rows in LOCKNUT_DATA.values():
        for row in rows:
            for field in LOCKNUT_VISIBLE_FIELDS:
                value = str(row.get(field, "")).lower()
                assert all(placeholder not in value for placeholder in LOCKNUT_PLACEHOLDER_TEXT)

            assert row["designation"]
            assert row["thread"]
            assert row["pitch_tpi"]
            assert row["matching_lock"]
            assert row["source_family"]
            assert row["programming_notes"]
